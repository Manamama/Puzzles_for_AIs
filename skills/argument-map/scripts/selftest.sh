#!/usr/bin/env bash
# Fixture check for this skill. Rebuilds the two bundled examples from scratch,
# asserts the pages are real, and asserts the validator still rejects a
# fabricated quote. Run after editing build.py, prep.py or the renderer.
#
#   bash scripts/selftest.sh [OUTDIR]        (default: $TMPDIR/argument-map-selftest)
#
set -euo pipefail

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
out="${1:-${TMPDIR:-/tmp}/argument-map-selftest}"
cd -- "$here"

rm -rf -- "$out"
mkdir -p -- "$out"
echo "skill dir: $here"
echo "scratch:   $out"

# 1. prep.py turns the raw thread dump into clean [Speaker] text.
python3 scripts/prep.py assets/example-thread-source.txt "$out/work"

# 2. Both worked examples must build with every span verified against its source.
python3 scripts/build.py assets/example-thread.json "$out/thread.html" --source "$out/work/source.txt"
python3 scripts/build.py assets/example.json "$out/single.html" --source assets/example-source.txt

for f in "$out/thread.html" "$out/single.html"; do
  [ -s "$f" ] || { echo "FAIL: $f missing or empty" >&2; exit 1; }
  if grep -q '/\*__DATA__\*/null' "$f"; then
    echo "FAIL: data placeholder survived in $f (renderer template not filled)" >&2; exit 1
  fi
  for tab in 'Argument map' 'Move timeline' 'Summary'; do
    grep -q "$tab" "$f" || { echo "FAIL: tab '$tab' missing from $f" >&2; exit 1; }
  done
done

# 3. Negative test: a quote that is not in the source must be refused, and
#    refused before anything is written. This is the guard that keeps the
#    model from inventing evidence.
python3 - "$out" <<'PY'
import json, sys
src = 'assets/example-thread.json'
data = json.load(open(src, encoding='utf-8'))
data['claims'][0]['span'] = 'a sentence nobody ever wrote, verbatim'
json.dump(data, open(sys.argv[1] + '/bad.json', 'w', encoding='utf-8'), ensure_ascii=False)
PY
if python3 scripts/build.py "$out/bad.json" "$out/bad.html" --source "$out/work/source.txt" >/dev/null 2>&1; then
  echo "FAIL: build.py accepted a span that does not occur in the source" >&2; exit 1
fi
if [ -e "$out/bad.html" ]; then
  echo "FAIL: build.py wrote output for an invalid map" >&2; exit 1
fi

# 4. wikitalk.py must recover the reply tree from the MediaWiki-DOM fixture.
#    Skipped (not failed) when beautifulsoup4 is absent: the core pipeline is stdlib-only.
if python3 -c 'import bs4' 2>/dev/null; then
  python3 scripts/wikitalk.py assets/example-wikitalk.html --section Test \
    --tree c-U-20260101120000 --outdir "$out/wt" > "$out/wt.log" 2>&1 || {
    echo "FAIL: wikitalk.py errored on the fixture (see $out/wt.log)" >&2; exit 1; }
  grep -q '^\[U\] First post says the opposite' "$out/wt/source.txt" &&
  grep -q '^\[V\] Reply: a reductio' "$out/wt/source.txt" &&
  [ "$(wc -l < "$out/wt/source.txt")" -eq 3 ] || {
    echo "FAIL: wikitalk.py lost the tree or the names (see $out/wt.log)" >&2; exit 1; }
  echo "PASS  wikitalk fixture: 3 comments, reply tree, names from User: links"
else
  echo "SKIP  wikitalk fixture (beautifulsoup4 not installed; core pipeline unaffected)"
fi

echo "PASS  2 examples built, 3 tabs present, fabricated quote rejected"
