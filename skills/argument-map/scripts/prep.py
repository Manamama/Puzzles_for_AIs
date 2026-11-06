#!/usr/bin/env python3
"""Turn a raw page dump into the clean, speaker-labelled source the skill works from.

usage: prep.py INPUT OUTDIR [--format auto|afd|forum|plain] [--speaker NAME]

Writes OUTDIR/source.txt  (one `[Speaker] text` line per post: no chrome, no quote chains,
                           no signatures, IP addresses anonymised)
       OUTDIR/posts.json  (id, speaker, when, stance, flags)
and prints a report. READ THE REPORT: speaker names are heuristics and must be eyeballed."""
import os, re, sys, json, collections

def die(m): sys.exit(m)

TS = re.compile(r'\d{1,2}:\d{2},? \d{1,2} [A-Z][a-z]+ \d{4} \(UTC\)')
IP = re.compile(r'^(?:\d{1,3}(?:\.\d{1,3}){3}|[0-9a-fA-F:]{12,})$')
TAILS = [r'\(\s*talk\s*(?:[•·]\s*contribs\s*)?\)', r'\(\s*t\s*·\s*c\s*\)', r'\|\s*reply here', r'/talk\b', r'\(Talk\)', r'\bTalk\)']
VOTE = re.compile(r'^(?:(?:strong|weak|speedy|snow)\s+)?(keep|delete|merge|redirect|comment|oppose|support|close)\b', re.I)

def stance(text):
    x = re.sub(r'^[\W_]+', '', text).lower()
    if re.match(r'(delete or merge|merge or delete|merge as suggested|delete/merge)', x): return 'delete/merge'
    m = VOTE.match(x)
    if not m: return None
    v = m.group(1).lower()
    return None if v in ('close', 'oppose', 'support') else {'redirect': 'merge'}.get(v, v)

class Anon:
    def __init__(s): s.m = {}
    def __call__(s, name):
        if IP.match(name):
            s.m.setdefault(name, 'IP editor ' + chr(65 + len(s.m) % 26))
            return s.m[name]
        return name

def split_sig(line, anon):
    """-> (speaker, text, when) for one signed wiki line."""
    m = TS.search(line)
    if not m: return None
    pre, when, rest = line[:m.start()].rstrip(), m.group(0), line[m.end():].strip()
    u = re.search(r'Preceding unsigned comment added by\s+(.+)$', pre)
    if u:
        name = re.sub(r'\(.*?\)', '', u.group(1)).strip() or '?'
        return anon(name), pre[:u.start()].rstrip(' —–-'), when
    clean = pre
    for t in TAILS: clean = re.sub(t, '', clean)
    clean = re.sub(r'(?<=\S)(--|—|–)(?=\s|[A-Za-z★])', r' \1', clean.rstrip())
    toks, got = clean.split(), []
    for tok in reversed(toks):
        stop = False
        if re.match(r'^(--|—|–|-{1,2})\S', tok): tok, stop = re.sub(r'^[-—–]+', '', tok), True
        elif tok in ('--', '—', '–', '-'): break
        elif re.search(r'[.!?:;"”)]$', tok) and got: break
        mm = re.match(r'^.*[a-z]{2}[.!?](?=[A-Z★0-9])(.+)$', tok)
        if mm: tok, stop = mm.group(1), True
        got.append(tok)
        if stop or len(got) >= 7: break
    name = re.sub(r'\s+at$', '', re.sub(r'^Posted by\s+', '', ' '.join(reversed(got)).strip())) or '?'
    idx = clean.rfind(got[-1]) if got else len(clean)
    text = clean[:idx].rstrip(' —–-') if got else clean
    return anon(name), (text + (' ' + rest if rest else '')).strip(), when

def parse_afd(lines, anon):
    a = next((i for i, l in enumerate(lines) if l.startswith('The result was')), None)
    b = next((i for i, l in enumerate(lines) if l.startswith('The above discussion is preserved')), len(lines))
    if a is None: die('AfD: no "The result was" line found')
    posts, warn = [], []
    for l in lines[a:b]:
        l = l.strip()
        if not l or l.startswith(('Note:', 'New to Articles', 'How to contribute', 'Introduction to', 'Guide to', 'Help, my')) \
           or re.search(r'\(edit\W+talk', l) or l.startswith('(Find sources') or re.match(r'^.+edit$', l) and len(l) < 60: continue
        sp = split_sig(l, anon)
        if l.startswith('The result was') and sp:
            posts.append({'speaker': 'Closer', 'text': sp[1], 'when': sp[2], 'kind': 'close', 'flags': []}); continue
        if sp and not sp[1].strip() and posts and posts[-1]['speaker'] == '?':
            posts[-1].update(speaker=sp[0], when=sp[2]); posts[-1]['flags'].append('signature on a later line; attributed to it'); continue
        if sp:
            posts.append({'speaker': sp[0], 'text': sp[1], 'when': sp[2], 'kind': 'comment', 'flags': []})
        elif posts and not stance(l):
            posts[-1]['text'] += ' ' + l; posts[-1]['flags'].append('continuation line merged')
        else:
            posts.append({'speaker': '?', 'text': l, 'when': '', 'kind': 'comment', 'flags': ['unsigned']})
    return posts, warn

def parse_forum(lines, anon):
    hdr = re.compile(r'^by (.+?) » (.+)$')
    idx = [i for i, l in enumerate(lines) if hdr.match(l)]
    if len(idx) < 2: die('forum: found fewer than 2 "by NAME » date" headers')
    raw = []
    for n, i in enumerate(idx):
        j = i + 1
        while j < len(lines) and lines[j].strip() != 'Top' and j < (idx[n + 1] if n + 1 < len(idx) else len(lines)): j += 1
        m = hdr.match(lines[i]); raw.append((m.group(1), m.group(2), [x.rstrip() for x in lines[i + 1:j] if x.strip()]))
    seen, posts = set(), []
    for who, when, body in raw:
        out, k, flags = [], 0, []
        while k < len(body):
            if re.search(r' wrote: ↑$', body[k]):
                k += 1
                if k < len(body) and re.match(r'^\w{3} \w{3} \d', body[k]): k += 1
                hit = 0
                while k < len(body) and body[k].strip() in seen: k += 1; hit += 1
                if not hit: flags.append('quote not found in earlier posts (kept as text; review)')
                continue
            out.append(body[k]); k += 1
        seen.update(x.strip() for x in body)
        posts.append({'speaker': anon(who), 'text': ' '.join(out).strip(), 'when': when, 'kind': 'comment', 'flags': flags, '_body': out})
    tails = collections.defaultdict(collections.Counter)      # repeated last lines per author = signatures
    for p in posts:
        if p['_body']: tails[p['speaker']][p['_body'][-1].strip()] += 1
    for p in posts:
        b = p['_body']
        while len(b) > 1 and tails[p['speaker']][b[-1].strip()] >= 2: b = b[:-1]
        p['text'] = ' '.join(x.strip() for x in b).strip(); del p['_body']
    return posts, []

def main():
    a = sys.argv[1:]
    def opt(name, dflt):
        """Reads --name VALUE wherever it appears on the line; removes both tokens."""
        if name not in a: return dflt
        i = a.index(name)
        if i + 1 >= len(a): die('%s needs a value' % name)
        v = a[i + 1]; del a[i:i + 2]; return v
    fmt = opt('--format', 'auto'); spk = opt('--speaker', 'Author')
    if len(a) != 2: die(__doc__)
    src_path, out_dir = a
    txt = open(src_path, encoding='utf-8').read(); lines = txt.splitlines(); anon = Anon()
    if fmt == 'auto':
        fmt = 'afd' if 'Articles for deletion' in txt[:400] else 'forum' if len(re.findall(r'^by .+ » ', txt, re.M)) >= 3 else 'plain'
    if fmt == 'afd': posts, _ = parse_afd(lines, anon)
    elif fmt == 'forum': posts, _ = parse_forum(lines, anon)
    else:
        posts = []
        for l in lines:
            m = re.match(r'^\[(.+?)\]\s+(.*)$', l)
            if m: posts.append({'speaker': m.group(1), 'text': m.group(2), 'when': '', 'kind': 'comment', 'flags': []})
            elif l.strip():
                if posts: posts[-1]['text'] += ' ' + l.strip()
                else: posts.append({'speaker': spk, 'text': l.strip(), 'when': '', 'kind': 'comment', 'flags': []})
    for i, p in enumerate(posts, 1):
        p['id'] = i; p['stance'] = stance(p['text']) if fmt == 'afd' and p['kind'] == 'comment' else None
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, 'source.txt'), 'w', encoding='utf-8').write(''.join('[%s] %s\n' % (p['speaker'], p['text']) for p in posts))
    json.dump(posts, open(os.path.join(out_dir, 'posts.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    c = collections.Counter(p['speaker'] for p in posts)
    print('format: %s | posts: %d | speakers: %d' % (fmt, len(posts), len(c)))
    print('speakers (CHECK these names): ' + ', '.join('%s(%d)' % kv for kv in c.most_common()))
    if fmt == 'afd':
        last = {}
        for p in posts:
            if p['stance'] and p['speaker'] not in ('?', 'Closer'): last[p['speaker']] = p['stance']
        first = next((p for p in posts if p['kind'] == 'comment'), None)
        if first and not first['stance']: last[first['speaker']] = 'delete (nominator)'
        t = collections.Counter(last.values())
        print('last explicit !vote per editor (approximate, by leading keyword): ' + ', '.join('%s %d' % kv for kv in t.most_common()))
        print('editors with no parsable vote: %d (e.g. "oppose", replies); count by hand if the tally matters' % (len(c) - len(last) - ('?' in c) - ('Closer' in c)))
    fl = [(p['id'], p['speaker'], f) for p in posts for f in p['flags']]
    print('flags: %d' % len(fl)); [print('  post %d [%s]: %s' % x) for x in fl[:12]]
main()
