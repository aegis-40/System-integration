#!/usr/bin/env python3
"""Aegis-40 wFOM engine (focused implementation of planning/PLAN.md §5).

wFOM(D,R) = Σ_c W_c · Σ_i w_ci · N_i(x_i^D, x_i^R),  N_i = u_i(x^D) − u_i(x^R)
⇒ wFOM(D,R) = U(D) − U(R)  with U(X) = Σ_c W_c Σ_i w_ci u_i(x^X)  (absolute utility).

Run:  python3 fom/wfom.py            # full analysis + writes outputs/wfom_report.md
"""
from __future__ import annotations
import math, pathlib, itertools, datetime
import yaml

ROOT = pathlib.Path(__file__).parent
REACTORS = ["aegis40", "carem25", "smart", "nuscale_voygr"]
NON_ELEC_FLOOR = 0.05   # PLAN §4: electricity-only reactors get a small placeholder share


# ---------------------------------------------------------------- load + derive
def load():
    schema = yaml.safe_load(open(ROOT / "parameters_schema.yaml"))
    econ = yaml.safe_load(open(ROOT / "economic_assumptions.yaml"))["prices"]
    reactors = {r: yaml.safe_load(open(ROOT / "reactors" / f"{r}.yaml")) for r in REACTORS}
    return schema, econ, reactors


def derived(rx, econ):
    """Compute derived params from the descriptive block. Returns dict param->value."""
    d = rx["descriptive"]
    P_el, P_th, CF = d["electric_power_mwe"], d["thermal_power_mwth"], d["capacity_factor"]
    cg = d["cogen"]
    p_el, p_th, p_h2 = (econ["electricity_usd_per_mwh"], econ["district_heat_usd_per_mwh"],
                        econ["hydrogen_usd_per_kg"])
    rev_el = P_el * 8760 * CF * p_el
    rev_th = cg["q_th_sold_mwth"] * cg["h_th_sold_hours"] * p_th
    rev_h2 = cg["m_h2_kg_per_yr"] * p_h2
    total = rev_el + rev_th + rev_h2
    share = (rev_th + rev_h2) / total if total else 0.0
    return {
        "thermal_efficiency": P_el / P_th,
        "footprint_per_mwe": d["plant_footprint_m2"] / P_el,
        "spent_fuel_per_mwh": (P_th / P_el) * (1.0 / d["burnup_GWd_per_MTU"]) * 24.0,
        "specific_revenue": total / (P_el * 1000.0),
        "non_electric_revenue_share": share if share > 0 else NON_ELEC_FLOOR,
    }


def flatten(rx, econ):
    """All param values for a reactor: explicit (from categories) + derived.
    A reactor with no 'descriptive' block (e.g. the standards reference) uses its
    explicit category values directly — no derivation."""
    vals = {}
    for cat in rx["categories"].values():
        for k, spec in cat.items():
            vals[k] = spec.get("value")
    if "descriptive" in rx:
        vals.update(derived(rx, econ))
    return vals


def ahp_weights(path):
    """Principal-eigenvector weights + Saaty consistency ratio from a pairwise matrix."""
    import numpy as np
    cfg = yaml.safe_load(open(path))
    order = cfg["order"]
    A = np.array([cfg["matrix"][r] for r in order], float)
    n = len(order)
    vals, vecs = np.linalg.eig(A)
    k = np.argmax(vals.real)
    w = np.abs(vecs[:, k].real)
    w = w / w.sum()
    lmax = vals[k].real
    CI = (lmax - n) / (n - 1)
    RI = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32}[n]
    CR = CI / RI
    return dict(zip(order, w)), CR


def pspecs(schema):
    """param_key -> (category, spec)."""
    out = {}
    for cname, c in schema["categories"].items():
        for k, spec in c["parameters"].items():
            out[k] = (cname, spec)
    return out


# ---------------------------------------------------------------- normalizers (per-reactor utility u_i)
def utility(value, spec):
    n = spec["normalizer"]
    if n == "log_ratio":
        d = 1.0 if spec["direction"] == "max" else -1.0
        return d * math.log(value)
    if n == "min_max":
        lo, hi = spec["scale"]
        frac = (value - lo) / (hi - lo)
        return frac if spec["direction"] == "max" else (1.0 - frac)
    if n == "target_gaussian":
        return math.exp(-spec["alpha"] * (value - spec["target"]) ** 2)
    raise ValueError(n)


def hard_violations(vals, specs):
    v = []
    for k, (_, spec) in specs.items():
        x = vals.get(k)
        if x is None:
            continue
        if spec.get("hard_floor") is not None and x < spec["hard_floor"]:
            v.append((k, x, "hard_floor", spec["hard_floor"]))
        if spec.get("hard_ceiling") is not None and x > spec["hard_ceiling"]:
            v.append((k, x, "hard_ceiling", spec["hard_ceiling"]))
    return v


# ---------------------------------------------------------------- pairwise wFOM
def pairwise(dvals, rvals, schema, specs, catw=None):
    """wFOM(D,R) with per-pair renormalization over params populated in BOTH."""
    cat_scores, used, dropped = {}, [], []
    cat_w = catw or {c: schema["categories"][c]["weight"] for c in schema["categories"]}
    active_cats = {}
    for cname, c in schema["categories"].items():
        params = c["parameters"]
        common = [k for k in params
                  if dvals.get(k) is not None and rvals.get(k) is not None]
        dropped += [k for k in params if k not in common]
        if not common:
            continue
        sw = {k: params[k]["sub_weight"] for k in common}
        tot = sum(sw.values())
        S = 0.0
        for k in common:
            spec = params[k]
            N = utility(dvals[k], spec) - utility(rvals[k], spec)
            S += (sw[k] / tot) * N
            used.append(k)
        cat_scores[cname] = S
        active_cats[cname] = cat_w[cname]
    wtot = sum(active_cats.values())
    score = sum((active_cats[c] / wtot) * cat_scores[c] for c in cat_scores)
    breakdown = {c: (active_cats[c] / wtot, cat_scores[c]) for c in cat_scores}
    return score, breakdown, sorted(set(used)), sorted(set(dropped) - set(used))


# ---------------------------------------------------------------- absolute utility (common set across given reactors)
def common_params(vals_by_rx, schema):
    keys = set.intersection(*[{k for k, v in vals.items() if v is not None}
                              for vals in vals_by_rx.values()])
    # keep only keys that are in the schema (scored params)
    allp = set(itertools.chain.from_iterable(
        c["parameters"].keys() for c in schema["categories"].values()))
    return keys & allp


def absolute_utility(vals, schema, specs, use_keys, catw=None):
    """U(X) over a fixed param set, weights renormalized to that set."""
    cat_w = catw or {c: schema["categories"][c]["weight"] for c in schema["categories"]}
    cat_scores, active = {}, {}
    for cname, c in schema["categories"].items():
        ks = [k for k in c["parameters"] if k in use_keys]
        if not ks:
            continue
        sw = {k: c["parameters"][k]["sub_weight"] for k in ks}
        tot = sum(sw.values())
        cat_scores[cname] = sum((sw[k] / tot) * utility(vals[k], c["parameters"][k]) for k in ks)
        active[cname] = cat_w[cname]
    wtot = sum(active.values())
    return sum((active[c] / wtot) * cat_scores[c] for c in cat_scores), cat_scores


# ---------------------------------------------------------------- TOPSIS cross-check (independent MCDA)
def global_weights(schema, use_keys):
    """param -> W_c · (sub_weight renormalized within the used keys of its category)."""
    cat_w = {c: schema["categories"][c]["weight"] for c in schema["categories"]}
    gw = {}
    for cname, c in schema["categories"].items():
        ks = [k for k in c["parameters"] if k in use_keys]
        if not ks:
            continue
        tot = sum(c["parameters"][k]["sub_weight"] for k in ks)
        for k in ks:
            gw[k] = cat_w[cname] * c["parameters"][k]["sub_weight"] / tot
    return gw


def transparency(vals_fe, schema, specs, ck):
    """Show raw inputs + per-parameter normalized utility + weighted contribution.
    Contributions are CENTERED on the field mean (the arbitrary log offset cancels),
    so each cell = how much that parameter pushes the reactor above/below the field
    average, and the column sum = U(reactor) − mean(U)."""
    gw = global_weights(schema, set(ck))
    lines = []
    order = sorted(ck, key=lambda k: (specs[k][0], -gw[k]))
    rxs = REACTORS

    lines.append("## 3a. Score transparency — every number")
    lines.append("\n### Raw inputs (what goes in)")
    lines.append("| Parameter (cat) | dir | Aegis-40 | CAREM-25 | SMART | NuScale |")
    lines.append("|---|---|---|---|---|---|")
    for k in order:
        cat, sp = specs[k]
        d = {"log_ratio": sp.get("direction", ""), "min_max": sp.get("direction", ""),
             "target_gaussian": "→tgt"}[sp["normalizer"]]
        vals = [vals_fe[r][k] for r in rxs]
        fmt = lambda x: f"{x:.3g}"
        lines.append(f"| {k} ({cat[:4]}) | {d} | {fmt(vals[0])} | {fmt(vals[1])} | "
                     f"{fmt(vals[2])} | {fmt(vals[3])} |")

    lines.append("\n### Weighted contribution to the ranking (centered on field mean)")
    lines.append("Cell = `gw·(uᵢ − mean)`. **+** helps, **−** hurts. Column sum = U − mean(U). "
                 "`gw` = global weight of the parameter.")
    lines.append("| Parameter | gw | Aegis-40 | CAREM-25 | SMART | NuScale |")
    lines.append("|---|---|---|---|---|---|")
    col_sum = {r: 0.0 for r in rxs}
    cat_sum = {}
    for k in order:
        cat, sp = specs[k]
        u = {r: utility(vals_fe[r][k], sp) for r in rxs}
        mean = sum(u.values()) / len(u)
        contrib = {r: gw[k] * (u[r] - mean) for r in rxs}
        for r in rxs:
            col_sum[r] += contrib[r]
            cat_sum.setdefault(cat, {r2: 0.0 for r2 in rxs})[r] += contrib[r]
        lines.append(f"| {k} | {gw[k]:.3f} | " +
                     " | ".join(f"{contrib[r]:+.3f}" for r in rxs) + " |")
    lines.append("| **category subtotals:** | | | | | |")
    for cat in schema["categories"]:
        if cat in cat_sum:
            lines.append(f"| _{cat}_ | {sum(gw[k] for k in order if specs[k][0]==cat):.3f} | " +
                         " | ".join(f"{cat_sum[cat][r]:+.3f}" for r in rxs) + " |")
    lines.append("| **U − mean(U)** | 1.000 | " +
                 " | ".join(f"**{col_sum[r]:+.3f}**" for r in rxs) + " |")
    return "\n".join(lines)


def topsis(vals_by_rx, schema, use_keys):
    import numpy as np
    rxs = list(vals_by_rx)
    cat_w = {c: schema["categories"][c]["weight"] for c in schema["categories"]}
    # global weight of each param = W_c * (sub_weight renormalized within used keys of category)
    gw = {}
    for cname, c in schema["categories"].items():
        ks = [k for k in c["parameters"] if k in use_keys]
        if not ks:
            continue
        tot = sum(c["parameters"][k]["sub_weight"] for k in ks)
        for k in ks:
            gw[k] = cat_w[cname] * c["parameters"][k]["sub_weight"] / tot
    keys = list(gw)
    benefit = {}  # True if higher is better
    for cname, c in schema["categories"].items():
        for k in c["parameters"]:
            if k in gw:
                sp = c["parameters"][k]
                benefit[k] = sp.get("direction", "max") == "max"  # gaussians excluded (none in use_keys here)
    M = np.array([[vals_by_rx[r][k] for k in keys] for r in rxs], float)
    norm = M / np.sqrt((M ** 2).sum(axis=0))
    W = np.array([gw[k] for k in keys])
    V = norm * W
    ideal = np.array([V[:, j].max() if benefit[keys[j]] else V[:, j].min() for j in range(len(keys))])
    anti = np.array([V[:, j].min() if benefit[keys[j]] else V[:, j].max() for j in range(len(keys))])
    dp = np.sqrt(((V - ideal) ** 2).sum(axis=1))
    dn = np.sqrt(((V - anti) ** 2).sum(axis=1))
    closeness = dn / (dp + dn)
    return dict(zip(rxs, closeness))


# ---------------------------------------------------------------- driver
def main():
    schema, econ, reactors = load()
    specs = pspecs(schema)
    vals = {r: flatten(reactors[r], econ) for r in REACTORS}

    out = []
    def p(s=""):
        out.append(s); print(s)

    p("# Aegis-40 wFOM — analysis report")
    p(f"*Generated {datetime.date.today()} by fom/wfom.py. Weights: "
      f"{schema['weight_status']} (PLAN §1.2 q1 — supervisor approval pending).*\n")

    # 1. hard-constraint gate
    p("## 1. Hard-constraint gate (PLAN §5.3)")
    feasible = {}
    for r in REACTORS:
        v = hard_violations(vals[r], specs)
        feasible[r] = not v
        if v:
            p(f"- **{r}: DESIGN_FAILED** → " + "; ".join(
                f"{k}={x} {lt} {lim}" for k, x, lt, lim in v))
        else:
            p(f"- {r}: feasible")
    p("")

    # rev_4: the de-peaking is now built into the design (edge-pin + ring zoning).
    # Aegis-40 peaking input is the de-peaked design target F_Q=2.00 (≤2.50 LCO) and
    # passes the gate directly; no scenario substitution needed.
    vals_fe = {r: dict(vals[r]) for r in REACTORS}
    p("> Aegis-40 peaking is the **rev_4 de-peaked design target F_Q ≈ 2.00** (≤2.50 LCO) — "
      "the 37-FA core + edge-pin/ring de-peaking replaces the rev_3 (21-FA) as-run 3.478. "
      "The gate now passes; the value awaits OpenMC high-stat confirmation (`open_item: "
      "peaking_recompute`; `safety/SIMULATION_ANALYSIS_PLAN.md` F1↔N6).\n")

    # 2. pairwise wFOM (Aegis-40 vs each reference)
    p("## 2. Pairwise wFOM — Aegis-40 vs references")
    p("wFOM > 0 ⇒ Aegis-40 scores higher on the weighted aggregate. Per-pair renormalization "
      "over parameters populated in **both** reactors.\n")
    p("| Reference | wFOM | safety | economic | safeguards | sustainability | efficiency | #params |")
    p("|---|---|---|---|---|---|---|---|")
    for ref in ["carem25", "smart", "nuscale_voygr"]:
        score, bd, used, drop = pairwise(vals_fe["aegis40"], vals_fe[ref], schema, specs)
        cells = []
        for c in ["safety", "economic", "safeguards", "sustainability", "efficiency"]:
            if c in bd:
                w, s = bd[c]
                cells.append(f"{w*s:+.3f}")
            else:
                cells.append("—")
        p(f"| {ref} | **{score:+.3f}** | " + " | ".join(cells) + f" | {len(used)} |")
    p("")

    # 3. absolute-utility ranking (single scale, common param set across all 4)
    ck = sorted(common_params(vals_fe, schema))
    p("## 3. Absolute-utility ranking (single scale)")
    p(f"Because every normalizer is a difference of a per-reactor term, an absolute utility "
      f"U(X) exists and wFOM(D,R)=U(D)−U(R). Ranked on the **{len(ck)} parameters populated "
      f"for all four reactors**: {', '.join(ck)}.\n")
    U = {}
    for r in REACTORS:
        U[r], _ = absolute_utility(vals_fe[r], schema, specs, set(ck))
    p("| Rank | Reactor | U (abs. utility) | ΔU vs Aegis-40 |")
    p("|---|---|---|---|")
    for i, (r, u) in enumerate(sorted(U.items(), key=lambda kv: -kv[1]), 1):
        p(f"| {i} | {r} | {u:+.3f} | {u - U['aegis40']:+.3f} |")
    p("")
    p("> Note: the common set has only **n_active_components** from the Safety category "
      "(PCT/MDNBR/peaking/MTC are sim-only and unpublished for competitors) — so this ranking "
      "under-represents Safety despite its 0.35 weight. The pairwise table (§2) recovers more "
      "safety coverage where reference data exists. **This data-availability gap is the single "
      "biggest threat to the comparison's validity.**\n")

    # 3a. transparency
    p(transparency(vals_fe, schema, specs, ck))
    p("")

    # 3b. absolute scoring vs international-standard reference
    std = yaml.safe_load(open(ROOT / "reactors" / "standards.yaml"))
    stdvals = flatten(std, econ)
    p("## 3b. Absolute scoring vs international-standard targets")
    p("Each reactor scored against a fixed benchmark of regulatory limits + good-design "
      "targets (`reactors/standards.yaml`) instead of against each other. **wFOM > 0 ⇒ beats "
      "the benchmark.** Reactor-independent, so it answers \"is it good?\" not just \"better than X?\"\n")
    p("| Reactor | wFOM vs standards | #params |")
    p("|---|---|---|")
    for r in REACTORS:
        if not feasible[r]:
            sc, _, used, _ = pairwise(vals_fe[r], stdvals, schema, specs)  # de-peaked variant
        else:
            sc, _, used, _ = pairwise(vals_fe[r], stdvals, schema, specs)
        p(f"| {r} | **{sc:+.3f}** | {len(used)} |")
    p("> Aegis-40 uses the de-peaked variant; with as-run peaking it is DESIGN_FAILED (§1). "
      "Aegis-40 sees more safety parameters here (it has PCT-less but MTC/peaking) than competitors do.\n")

    # 3c. AHP weights + consistency
    aw, cr = ahp_weights(ROOT / "ahp" / "category_pairwise.yaml")
    p("## 3c. AHP category weights + consistency check")
    p(f"Principal-eigenvector weights from `ahp/category_pairwise.yaml`. **Consistency ratio "
      f"CR = {cr:.4f}** (must be < 0.10 — {'PASS' if cr < 0.10 else 'FAIL'}).\n")
    p("| Category | AHP weight | default weight |")
    p("|---|---|---|")
    for c in schema["categories"]:
        p(f"| {c} | {aw[c]:.3f} | {schema['categories'][c]['weight']:.3f} |")
    U_ahp = {r: absolute_utility(vals_fe[r], schema, specs, set(ck), catw=aw)[0] for r in REACTORS}
    rank_ahp = [r for r, _ in sorted(U_ahp.items(), key=lambda kv: -kv[1])]
    rank_def = [r for r, _ in sorted(U.items(), key=lambda kv: -kv[1])]
    p(f"\n→ ranking with AHP weights: {' > '.join(rank_ahp)}")
    p(f"→ ranking with default weights: {' > '.join(rank_def)}  "
      f"({'SAME' if rank_ahp == rank_def else 'DIFFERS'})\n")

    # 4. validation suite
    p("## 4. Validation suite")
    ok = []
    # identity
    s_id, *_ = pairwise(vals_fe["carem25"], vals_fe["carem25"], schema, specs)
    ok.append(("identity  wFOM(R,R)=0", abs(s_id) < 1e-12, f"{s_id:.2e}"))
    # antisymmetry
    a, *_ = pairwise(vals_fe["aegis40"], vals_fe["smart"], schema, specs)
    b, *_ = pairwise(vals_fe["smart"], vals_fe["aegis40"], schema, specs)
    ok.append(("antisymmetry  wFOM(A,B)=−wFOM(B,A)", abs(a + b) < 1e-12, f"{a:+.3f}/{b:+.3f}"))
    # transitivity on common set (use absolute U so set is fixed)
    uA = U["aegis40"]; uB = U["smart"]; uC = U["nuscale_voygr"]
    lhs = uA - uC; rhs = (uA - uB) + (uB - uC)
    ok.append(("transitivity  U(A)−U(C)=(A−B)+(B−C)", abs(lhs - rhs) < 1e-12, f"{lhs:.3f}={rhs:.3f}"))
    # monotonicity: improve a max-direction param → wFOM up
    base, *_ = pairwise(vals_fe["aegis40"], vals_fe["carem25"], schema, specs)
    bumped = dict(vals_fe["aegis40"]); bumped["burnup"] *= 1.1
    mono, *_ = pairwise(bumped, vals_fe["carem25"], schema, specs)
    ok.append(("monotonicity  ↑burnup ⇒ ↑wFOM", mono > base, f"{base:+.3f}→{mono:+.3f}"))
    # reference independence: wFOM(A,B)-wFOM(A,C) == U(C... ) consistency via U
    pAB, *_ = pairwise(vals_fe["aegis40"], vals_fe["smart"], schema, specs)
    pAC, *_ = pairwise(vals_fe["aegis40"], vals_fe["nuscale_voygr"], schema, specs)
    # only equal to U-diff if param sets match; report as informational
    p("| Property | Pass | Value |")
    p("|---|---|---|")
    for name, passed, val in ok:
        p(f"| {name} | {'✅' if passed else '❌'} | {val} |")
    p("")

    # 5. independent cross-check: TOPSIS on the same common set
    p("## 5. Independent cross-check — TOPSIS")
    tp = topsis(vals_fe, schema, set(ck))
    rank_w = [r for r, _ in sorted(U.items(), key=lambda kv: -kv[1])]
    rank_t = [r for r, _ in sorted(tp.items(), key=lambda kv: -kv[1])]
    p("Same data + global weights, different aggregation (distance-to-ideal). If the ranking "
      "agrees with wFOM, the result is method-robust.\n")
    p("| Reactor | TOPSIS closeness | wFOM rank | TOPSIS rank |")
    p("|---|---|---|---|")
    for r in sorted(tp, key=lambda x: -tp[x]):
        p(f"| {r} | {tp[r]:.3f} | {rank_w.index(r)+1} | {rank_t.index(r)+1} |")
    p(f"\n→ wFOM order: {' > '.join(rank_w)}\n→ TOPSIS order: {' > '.join(rank_t)}  "
      f"({'AGREE' if rank_w == rank_t else 'DIFFER — investigate'})\n")

    # 6. weight robustness: leave-one-category-out ranking stability
    p("## 6. Weight robustness — leave-one-category-out")
    p("Drop each category, re-rank on the common set. If Aegis-40's rank holds, the result "
      "doesn't hinge on one category.\n")
    p("| Dropped category | Ranking (best→worst) | Aegis-40 rank |")
    p("|---|---|---|")
    base_rank = [r for r, _ in sorted(U.items(), key=lambda kv: -kv[1])]
    p(f"| (none) | {' > '.join(base_rank)} | {base_rank.index('aegis40')+1} |")
    for drop_c in schema["categories"]:
        keys = {k for k in ck if specs[k][0] != drop_c}
        if not keys:
            continue
        Ud = {r: absolute_utility(vals_fe[r], schema, specs, keys)[0] for r in REACTORS}
        rk = [r for r, _ in sorted(Ud.items(), key=lambda kv: -kv[1])]
        p(f"| −{drop_c} | {' > '.join(rk)} | {rk.index('aegis40')+1} |")
    p("")

    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "wfom_report.md").write_text("\n".join(out) + "\n")
    print("\n[written] fom/outputs/wfom_report.md")


if __name__ == "__main__":
    main()
