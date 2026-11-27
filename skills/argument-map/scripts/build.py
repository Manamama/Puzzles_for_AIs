#!/usr/bin/env python3
"""Validate argument-map JSON and build a self-contained HTML file.

Usage: python build.py map.json out.html [--source source.txt]
Exit code 0 = built (warnings may print), 2 = validation errors (nothing written).
"""
import json
import os
import re
import sys

REL_TYPES = {"supports", "undermines", "undercuts", "rebuts"}
KNOWN_KINDS = {"premise", "warrant", "backing", "qualifier", "conclusion",
               "counter", "concession", "claim"}
PLACEHOLDER = "/*__DATA__*/null"


def norm(s):
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2026", "...")
    return re.sub(r"\s+", " ", s).strip().casefold()


def check_conf(obj, where, errors):
    c = obj.get("conf")
    if c is not None and not (isinstance(c, (int, float)) and 0 <= c <= 1):
        errors.append(f"{where}: conf must be a number between 0 and 1")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    source = None
    if "--source" in argv:
        i = argv.index("--source")
        src_path = argv[i + 1]
        args = [a for a in args if a != src_path]
        with open(src_path, encoding="utf-8") as f:
            raw_source = f.read()
            source = norm(raw_source)
    if len(args) != 2:
        print(__doc__)
        return 2
    in_path, out_path = args

    with open(in_path, encoding="utf-8") as f:
        data = json.load(f)

    errors, warns = [], []
    ROLES = {"question", "position", "evidence", "concession", "agreement", "procedural", "other"}
    claims = data.get("claims") or []
    if len(claims) < 2:
        errors.append("need at least 2 claims")
    ids = set()
    for i, c in enumerate(claims):
        w = f"claim[{i}] {c.get('id', '?')}"
        if not c.get("id") or not c.get("text"):
            errors.append(f"{w}: id and text are required")
            continue
        if c["id"] in ids:
            errors.append(f"{w}: duplicate id")
        ids.add(c["id"])
        src = c.get("source", "stated")
        if src not in ("stated", "reconstructed"):
            errors.append(f"{w}: source must be 'stated' or 'reconstructed'")
        if c.get("kind") and c["kind"] not in KNOWN_KINDS:
            warns.append(f"{w}: unusual kind '{c['kind']}'")
        if src == "stated" and not c.get("span"):
            errors.append(f"{w}: stated claim needs a verbatim span")
        if len(c["text"].split()) > 28:
            warns.append(f"{w}: text is long; keep claims to one short sentence")
        check_conf(c, w, errors)

    for i, r in enumerate(data.get("relations") or []):
        w = f"relation[{i}]"
        if r.get("type") not in REL_TYPES:
            errors.append(f"{w}: type must be one of {sorted(REL_TYPES)}")
        for k in ("from", "to"):
            if r.get(k) not in ids:
                errors.append(f"{w}: '{k}' = {r.get(k)!r} is not a claim id")
        check_conf(r, w, errors)
    if not data.get("relations"):
        errors.append("no relations: an argument map needs at least one edge")

    for i, m in enumerate(data.get("moves") or []):
        w = f"move[{i + 1}]"
        if not m.get("who"):
            errors.append(f"{w}: who is required")
        lv = m.get("level")
        if not (isinstance(lv, int) and 0 <= lv <= 7):
            errors.append(f"{w}: level must be an integer 0 to 7")
        if not m.get("span"):
            errors.append(f"{w}: span is required")
        if m.get("target") and m["target"] not in ids:
            errors.append(f"{w}: target {m['target']!r} is not a claim id")
        if m.get("role") and m["role"] not in ROLES:
            warns.append(f"{w}: unusual role {m['role']!r}; use one of {sorted(ROLES)}")
        if lv == 0 and not m.get("role"):
            warns.append(f"{w}: level 0 without a role (question, position, evidence, concession, agreement, procedural)")
        check_conf(m, w, errors)
    # lint: a level-0 move whose speaker also attacks the same target is probably mis-graded
    rels = data.get("relations") or []
    by_id = {c.get("id"): c for c in claims}
    for i, m in enumerate(data.get("moves") or []):
        if m.get("level") == 0 and m.get("target"):
            for r in rels:
                if r.get("to") == m["target"] and r.get("type") != "supports" and by_id.get(r.get("from"), {}).get("who") == m.get("who"):
                    warns.append(f"move[{i + 1}]: graded 0 but {m['who']} also has an attacking relation on {m['target']}; check the level")
                    break
    grp = data.get("groups") or {}
    for who_, g in grp.items():
        if who_ not in (data.get("participants") or []):
            warns.append(f"groups: {who_!r} is not listed in participants")
    if len(claims) > 18:
        warns.append("more than 18 claims: split into per-issue maps")
    for i, wp in enumerate(data.get("weak_points") or []):
        if wp.get("claim") not in ids:
            errors.append(f"weak_points[{i}]: claim {wp.get('claim')!r} unknown")
    if len(data.get("weak_points") or []) > 6:
        warns.append("more than 6 weak points; keep only the ones that matter")
    for u in data.get("unanswered") or []:
        if u not in ids:
            errors.append(f"unanswered: {u!r} is not a claim id")

    if source is not None:
        spans = [("claim " + c.get("id", "?"), c.get("span")) for c in claims]
        spans += [(f"move {i + 1}", m.get("span"))
                  for i, m in enumerate(data.get("moves") or [])]
        blocks = {}
        for line in raw_source.splitlines():
            mm = re.match(r"^\[(.+?)\]\s?(.*)$", line)
            if mm:
                blocks.setdefault(mm.group(1), []).append(norm(mm.group(2)))
        owners = [(c.get("who"), c.get("source", "stated")) for c in claims] + \
                 [(m.get("who"), "stated") for m in (data.get("moves") or [])]
        for (where, sp), (who_, kind) in zip(spans, owners):
            if not sp:
                continue
            if norm(sp) not in source:
                errors.append(f"{where}: span not found in source: {sp[:70]!r}")
            elif kind == "stated" and who_ in blocks and not any(norm(sp) in b for b in blocks[who_]):
                warns.append(f"{where}: span exists, but not in a post by {who_}; check attribution")
    else:
        warns.append("no --source given: spans were NOT verified")

    for e in errors:
        print("ERROR  " + e)
    for w in warns:
        print("WARN   " + w)
    if errors:
        print(f"\n{len(errors)} error(s); nothing written.")
        return 2

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "assets", "renderer.html"), encoding="utf-8") as f:
        tpl = f.read()
    if PLACEHOLDER not in tpl:
        print("ERROR  renderer.html is missing the data placeholder")
        return 2
    blob = json.dumps(data, ensure_ascii=False)
    blob = blob.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    html = tpl.replace(PLACEHOLDER, blob, 1)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    n_m = len(data.get("moves") or [])
    print(f"OK  {len(claims)} claims, {len(data['relations'])} relations, "
          f"{n_m} moves, {len(warns)} warning(s) -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
