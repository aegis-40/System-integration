# TASK_PROCESS.md — how to tackle any new scope

*A reusable 7-step recipe distilled from Week 1. Apply to every FER section, every weekly assignment, every new responsibility. The discipline is what kept Week 1's deliverables internally consistent under cross-audit.*

*Read this once. Reread it before starting each new scope.*

---

## The recipe in one glance

```
1. SPEC      — read what the FER actually asks for
2. INPUTS    — gather what others have produced + what you have to assume
3. DECISIONS — lock the structural choices BEFORE planning the work
4. PLAN      — write a day-by-day file before you write any deliverable
5. EXECUTE   — produce artifacts in the right folder with the right naming
6. AUDIT     — adversarial self-review before anyone else sees it
7. BRIEF     — write the spoken script for the meeting
```

Every Week 1 deliverable that survived audit followed all seven. Every defect caught in audit came from skipping one.

---

## 1. SPEC — what does the FER actually ask?

**Open `docs/FER_Template.docx` to the §8.x section you're responsible for.** Read it twice. The second pass: decompose into discrete numbered requirements. Each "must be presented", "must be described", "must be demonstrated" is a separate requirement.

Output a private list:
```
R1 — overview of system
R2 — list of components
R3 — diagram of connections
R4 — performance characterized
...
```

This list becomes the **coverage table** you'll build in step 6. You did this for §8.7 — see `ic/fer_8_7_coverage.md`. Twenty-five discrete requirements emerged from what looked like four paragraphs.

**Anti-pattern:** start writing before you've decomposed. You'll cover 80 %, miss the four sentences a reviewer notices.

---

## 2. INPUTS — what's already known and what must you assume?

Three buckets:

### 2a. Locked inputs (use, don't redo)
- `docs/FER_Template.docx` — Table 1 numbers (illustrative — see locked-decisions in `README.md`)
- `docs/PER_NUClearly.pdf` — historical commitments
- `planning/MEETING_BRIEF.md` — supervisor-set defaults
- Other teams' frozen outputs in their own folders
- The `decisions_locked` block in `safety/safety_criteria.yaml`

### 2b. Pending inputs (need from teammates)
- Identify *which teammate produces what number* you need.
- Send the ask **on day 1**, not day 4. Async lag is the dominant cost.
- Keep a short table in your plan: *who · what · by when · what it blocks*.

### 2c. Assumptions you'll make (because no one has produced them yet)
- Write each assumption explicitly: *parameter · value · source / rationale · how to verify later*.
- Tag everything you place in deliverables with `[ASSUMED]` or `[SIM-PENDING]` so it's visible. Later swap is then one grep.

**Anti-pattern:** invent a number and forget it was invented. Two months later it appears in the FER as fact.

---

## 3. DECISIONS — lock structure before content

Before writing any content, identify the **3–7 structural choices** that, if changed later, would force a rewrite. Examples from Week 1:
- Cladding (Zr-2 vs Zr-4) — changes oxidation row, neutron economy
- Soluble-boron status — changes shutdown-margin source, ATWS branch
- Event-tree initiator (SBO vs LOHS) — changes what's demonstrated
- Drawing tool (Mermaid vs draw.io) — changes file format

For each: decide once, write the rationale, lock it in either:
- `README.md` "Locked design decisions" table (project-wide), or
- the scope's plan file `decisions_locked` block (scope-local).

If a decision is supervisor-blocked, write it as **open item** with owner + by-when.

**Why this step:** rewrites are the most expensive thing. A 15-minute decision conversation upfront saves a 4-hour rewrite later.

**Anti-pattern:** start writing assuming "we'll figure it out as we go." You write 8 pages, the choice flips, six of those pages need redo.

---

## 4. PLAN — day-by-day file, written first

Create `planning/W?_<scope>_Plan.md` before touching a deliverable. Required sections:

| Section | Content |
|---|---|
| **Goal of the week** | One sentence. What ships by Friday. |
| **Hard deliverables** | Numbered list. Each item = one file with a name. |
| **Stretch deliverables** | Optional bonus list. Move to next week if pushed. |
| **Day-by-day schedule** | Day 1 ... Day 7. Each day = output + time estimate. |
| **Coordination** | Table: person, what I need, by when, why. |
| **Standards / references** | Bibliography you'll cite while writing. |
| **Risks + mitigations** | What could derail this; how you'll absorb it. |
| **Files this week creates** | Tree of paths to be born. |
| **FER mapping** | Which §8.x each artifact lands in. |
| **EOW self-check** | Tick-boxes you'll verify before declaring done. |

Reference: `planning/W1_Plan.md` is the worked example.

**Time on plan: ~1–2 h.** Cheap relative to what it prevents.

---

## 5. EXECUTE — discipline of where things land

### 5a. File naming + location
- Each scope has a folder (`safety/`, `ic/`, `fom/`, `layout/`). Deliverables go in the matching folder.
- Names are **lowercase_with_underscores.{ext}**. No spaces, no capitals.
- Sources (YAML) are authoritative; renders (MD, PNG) derive from sources.
- Diagrams: `<name>.mmd` (source) + `<name>.png` (rendered). Keep both.

### 5b. Cross-references
- Inside a doc, refer to other artifacts by **repo-root-relative path**: `safety/safety_criteria.yaml`.
- Every deliverable's header carries a **FER §8.x mapping** + companion-files line.
- Every numeric value's *source* (regulation, simulation, assumption) is named in the row.

### 5c. The single-source-of-truth rule
- **YAML over MD.** Numbers live in YAML; MD is a render. Never edit MD-only.
- If a value appears in 2+ files, one is canonical; the others derive from it. The canonical location goes in `README.md`.
- This is what kept the Week 1 audit clean. Drift between docs is the #1 defect type in safety submissions.

### 5d. Daily updates
- End each working day: update the scope's `_INDEX.md` if new files landed.
- Mark task-tracker items done as you go (not at week-end).

**Anti-pattern:** put diagrams in `docs/` because they're "documentation." `docs/` is for *external source documents*. Your output goes in the scope folder.

---

## 6. AUDIT — adversarial self-review

Before claiming done, run **two passes**:

### 6a. Mid-week self-review (Wed evening, ~30 min)
Pretend you're a senior engineer who didn't write this:
- Does each requirement (from step 1's decomposition) have a real answer, not just a paragraph?
- Are the numbers physically sensible? (e.g. pressure ladder ordered correctly: operating < trip < design)
- Are there any *contradictions* between this artifact and another?
- Are units stated everywhere? Are signs (negative MTC) explicit?
- Does every claim have a citation, sim source, or "[ASSUMED]" tag?

Output: a list of fixes; apply same evening.

### 6b. End-week cross-artifact audit (Fri, ~1 h)
Mechanical checks across all artifacts:
- All cross-references resolve (every `#21` is in some inventory; every `setpoint_link` is in some trip file)
- All counts match (if you claim "27 criteria," count them)
- Numeric ladders coherent (operating < trip < design pressures, etc.)
- No orphan terms (something appears in one doc, nowhere else)
- Internal counts in summaries match the items listed

Output: a graded findings list (✓ / △ / ✗ / 🐞).
Fix everything 🐞 and ✗ immediately. △ either fix or log to next week.

**Reference:** `ic/fer_8_7_coverage.md` is the worked example — 25 discrete checks, status per check.

**Anti-pattern:** declare done because the deliverable file *exists*. Existence ≠ correctness.

---

## 7. BRIEF — the spoken script

Build a **meeting-ready briefing** in `planning/briefings/MB_<period>.md`. Either:
- Daily after a big chunk (`MB_D1.md`, `MB_D3.md`)
- End-of-week summary (`MB_W1.md`)

Required:
- Timing budget per section (target 5–15 min)
- `>` quote blocks = verbatim spoken text
- `[stage directions]` = what to point at on screen
- Backup Q&A with anticipated questions + scripted answers

**Why:** explaining your work *out loud* exposes weak spots you'd never see in writing. If a sentence is hard to say, the underlying claim is probably soft. Rewrite both.

Reference: `planning/briefings/MB_W1.md`.

---

## Cadence template (one week)

| Day | Activity |
|---|---|
| Mon | Step 1 (spec read) + Step 2 (inputs + pings sent) + Step 3 (decisions locked) + Step 4 (plan written). End-of-day: plan file exists. |
| Tue | Execute first deliverable. |
| Wed | Execute second; **mid-week self-review** (step 6a). |
| Thu | Execute third; respond to teammate inputs as they land. |
| Fri | Execute fourth + **cross-artifact audit** (step 6b) + apply fixes. |
| Sat | Buffer + briefing draft. |
| Sun | Brief finalized; week ready. |

Adjust to scope size, but **the seven steps don't move.**

---

## When something goes off the rails

| Symptom | Likely missing step | Quick fix |
|---|---|---|
| "I don't know what FER expects" | Step 1 incomplete | Re-decompose §8.x; rebuild requirement list |
| "I have to redo this whole document" | Step 3 skipped | Identify which structural choice changed; lock it now; don't re-redo |
| "The numbers in two docs disagree" | Step 5c violated | Pick the canonical location; delete the other or auto-derive |
| "The teammate I need is silent" | Step 2b late | Send the ask now with an explicit by-when |
| "Supervisor caught a defect" | Step 6 skipped | Audit *before* meeting, not after |
| "I forgot what we decided" | Step 3 not logged | Add to README locked-decisions table |

---

## What this process is NOT

- It is not waterfall. Steps overlap; later steps loop back to earlier ones when new info arrives.
- It is not a substitute for engineering judgment. The process organizes thinking; it doesn't replace thinking.
- It is not optional. The Week 1 audit caught six defects across artifacts that nominally "looked done." Without the process, those land in the FER.

---

## Quick links

- Worked plan example: `planning/W1_Plan.md`
- Worked audit example: `ic/fer_8_7_coverage.md`
- Worked briefing example: `planning/briefings/MB_W1.md`
- Source-of-truth example: `safety/safety_criteria.yaml`

---

*Maintained by Azamhon. Update this file when a new step proves necessary. Don't bloat — every step earned its place by catching a real defect.*
