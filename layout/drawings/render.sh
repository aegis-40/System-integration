#!/usr/bin/env bash
# Rasterize an SVG to PNG via chrome-headless-shell (same engine as the mermaid pipeline).
# SVG must carry explicit pixel width/height on its root <svg> element.
# Usage: ./render.sh FILE.svg WIDTH HEIGHT   (W/H = the SVG's px width/height)
set -euo pipefail

SVG="$1"; W="$2"; H="$3"
OUT="${SVG%.svg}.png"

CHROME="$HOME/.cache/puppeteer/chrome-headless-shell/mac_arm-149.0.7827.22/chrome-headless-shell-mac-arm64/chrome-headless-shell"
[ -x "$CHROME" ] || CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ABS="$(cd "$(dirname "$SVG")" && pwd)/$(basename "$SVG")"

"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 \
  --window-size="${W},${H}" \
  --screenshot="$OUT" \
  "file://${ABS}" >/dev/null 2>&1

echo "rendered $OUT ($(($W*2))x$(($H*2)) px @2x)"
