#!/usr/bin/env python3
"""Recover the real reply tree from a MediaWiki discussion page saved from the browser
(Ctrl+S on the rendered thread).

This is a helper with a narrow contract, not a general importer — see
references/ingest.md for the three input routes and what to adapt by hand.
What is stable: MediaWiki's DiscussionTools marker attributes and comment ids,
  <span data-mw-comment-start id="c-<acct>-<YYYYMMDDHHMMSS>-<parent acct>-<parent ts>">
which are code-level and survive wiki localization. The id gives speaker, timestamp
and *which comment it answers*; a null tail means a thread root. Ids embed only one
level of parentage, so the parent is looked up by (account, timestamp), never by
string prefix. Visible signature names come from the "User:" link, not the id,
because accounts and signatures differ (F0malhaut42 signs as ғѳmɑɭʱɑυե).
What is NOT stable, and is deliberately kept heuristic: signature decoration and
the UI strings around it ("talk", "contribs" — localized into every wiki language,
so on a non-English wiki extend clean_name rather than trust it). Other sites'
discussion backends have no markers at all: write [Speaker] text by hand.
Requires beautifulsoup4 + lxml (the only non-stdlib dependency in this skill).

usage:
  wikitalk.py FILE --section TEXT [--outline N|all] [--posts OUT.json] [--grep TEXT]
  wikitalk.py FILE --section TEXT --tree ID [--outdir DIR]

  --section TEXT   heading substring, e.g. "Anti-Defamation"
  --outline N      indented outline, N comments ("all" for every one)
  --tree ID        that comment and all descendants, indented
  --outdir DIR     with --tree: also write source.txt + posts.json in [Speaker] form
  --posts FILE     write every comment as JSON
"""
import json
import os
import re
import sys
from bs4 import BeautifulSoup, NavigableString

TS = re.compile(r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$')
def split_id(cid):
    """c-acct-20261029163100-parentacct-20261029120800 -> (acct, when, parentkey)."""
    if not cid or not cid.startswith('c-'):
        return None
    parts = cid[2:].split('-')
    idx = [i for i, p in enumerate(parts) if TS.match(p)]
    if not idx:
        return None
    i_self = idx[0]
    m = TS.match(parts[i_self])
    when = '%s-%s-%s %s:%s' % m.groups()[:5]
    acct = '-'.join(parts[:i_self])
    parent = None
    if len(idx) > 1:
        i_par = idx[1]
        parent = ('-'.join(parts[i_self + 1:i_par]), '%s-%s-%s %s:%s' % TS.match(parts[i_par]).groups()[:5])
    return acct, when, parent


# Page-specific signature variants -> one handle, added per export as they are seen
# (custom sigs, decorations, translated "(talk)" labels). CHECK after every page.
NAMES = {}


def clean_name(s):
    """Signature blob -> display name. Names are heuristics: eyeball them."""
    s = re.sub(r'[\u2003\u00a0]+', ' ', s).strip()
    s = re.sub(r'\s*\((?:talk|\?talk|contribs|t|TALK\s*PAGE|Talk[·•]Contribs|Any pronouns|'
               r'you just lost the game)\)\s*', ' ', s, flags=re.I)
    s = s.replace('\u1d40\u1d43\u1d38', '').replace('\u1d40\u1d43 \u1d38', '')
    s = re.sub(r'^(?:--|\u2014|\u2013|\u2190|\u2022)\s*', '', s.strip())
    s = re.sub(r'^User:', '', s)
    s = re.sub(r',\s*Ret\.$', '', s)
    s = re.sub(r'[\u1d40\u1d43\u02e1\u1d4f]+$', '', s).strip()   # superscript 'Talk'
    s = s.strip('\ua981\ua982\ua9c2\ua9c3 ')                     # Mangroves' crowns
    return NAMES.get(s.replace('_', ' '), re.sub(r'\s+', ' ', s).strip(' ,'))


def speaker_of(marker, fallback):
    """The signature lives between the sig marker and the timestamp link.
    Joined with '' because templates split names across nodes ('M'+'asem').
    Stops at the first nested reply container so children's sigs are not read."""
    if marker is None:
        return fallback
    parts = []
    for el in marker.next_elements:
        if getattr(el, 'name', None) in ('dd', 'dl', 'li', 'table', 'section'):
            break
        cls = ' '.join(el.get('class') or []) if getattr(el, 'name', None) else ''
        if 'timestamplink' in cls:
            break
        if isinstance(el, NavigableString):
            parts.append(str(el))
    return clean_name(''.join(parts)) or fallback


def body_text(dd, marker):
    """Text of this comment only: everything before its signature marker.
    Nested replies live after that marker, so they are excluded for free."""
    parts = []
    for el in dd.descendants:
        if el is marker:
            break
        if isinstance(el, NavigableString):
            t = str(el)
            if t.strip():
                parts.append(t)
    txt = re.sub(r'[\u2003\u00a0]+', ' ', ' '.join(parts))
    return re.sub(r'\s+', ' ', txt).strip(' ,')


def load(path, section_text):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'lxml')
    sec = None
    for s in soup.find_all('section'):
        h = s.find(['h2', 'h3', 'h4'])
        if h and section_text.casefold() in h.get_text(' ', strip=True).casefold():
            sec = s
            break
    if sec is None:
        sys.exit('section not found: %r' % section_text)
    heading = sec.find(['h2', 'h3', 'h4']).get_text(' ', strip=True)

    post, bykey = {}, {}
    for span in sec.select('span[data-mw-comment-start]'):
        cid = span.get('id')
        info = split_id(cid)
        if not info:
            continue
        acct, when, parentkey = info
        dd = span.find_parent(['dd', 'li'])
        if dd is None:
            continue
        marker = dd.select_one('span[data-mw-comment-sig]')
        post[cid] = {'id': cid, 'speaker': speaker_of(marker, acct), 'acct': acct,
                     'when': when, 'parent': None, 'children': [],
                     'text': body_text(dd, marker)}
        bykey[(acct, when)] = cid

    roots = []
    for cid, c in post.items():
        acct, when, parentkey = split_id(cid)
        pid = bykey.get(parentkey) if parentkey else None
        if pid and pid != cid:
            c['parent'] = pid
            post[pid]['children'].append(cid)
        else:
            roots.append(cid)
    order = list(post)
    for c in post.values():
        c['children'].sort(key=order.index)

    return heading, post, roots, order


def walk(post, ids, depth=0):
    order = list(post)
    def rec(cid, d):
        if cid in ids:
            yield d, post[cid]
        for k in post[cid]['children']:
            yield from rec(k, d + 1)
    for r in order:
        if post[r]['parent'] is None:
            yield from rec(r, 0)


def subtree(post, root):
    out, seen, stack = set(), set(), [root]
    while stack:
        cid = stack.pop()
        if cid in seen:
            continue
        seen.add(cid)
        out.add(cid)
        stack.extend(post[cid]['children'])
    return out


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)

    def opt(name, dflt=None):
        if name not in a:
            return dflt
        i = a.index(name)
        v = a[i + 1]
        del a[i:i + 2]
        return v

    section, outline = opt('--section'), opt('--outline')
    pjson, grep, tree = opt('--posts'), opt('--grep'), opt('--tree')
    outdir, path = opt('--outdir'), a[0]

    heading, post, roots, order = load(path, section)
    print('# %s' % heading)
    print('# %d comments, %d thread roots, %d speakers' % (
        len(post), len(roots), len({c['speaker'] for c in post.values()})))

    if pjson:
        json.dump([post[c] for c in order], open(pjson, 'w', encoding='utf-8'),
                  indent=1, ensure_ascii=False)
        print('# wrote %s' % pjson)

    rows = list(walk(post, set(post)))

    if grep:
        for d, c in rows:
            if grep.casefold() in c['text'].casefold() or grep.casefold() in c['speaker'].casefold():
                print('%s%s %s  %s' % ('  ' * d, c['speaker'], c['when'], c['text'][:100]))
                print('%s  id=%s' % ('  ' * d, c['id']))
        return

    if tree:
        ids = subtree(post, tree)
        sel = [(d, c) for d, c in rows if c['id'] in ids]
        print('# subtree of %s: %d comments, %d speakers' % (
            tree, len(sel), len({c['speaker'] for _, c in sel})))
        for d, c in sel:
            print('%s- %s %s: %s' % ('  ' * d, c['speaker'], c['when'], c['text'][:150]))
        if outdir:
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, 'source.txt'), 'w', encoding='utf-8') as f:
                for _, c in sel:
                    f.write('[%s] %s\n' % (c['speaker'], c['text']))
            json.dump([c for _, c in sel],
                      open(os.path.join(outdir, 'posts.json'), 'w', encoding='utf-8'),
                      indent=1, ensure_ascii=False)
            print('# wrote %s/source.txt (%d posts) + posts.json' % (outdir, len(sel)))
        return

    if outline is not None:
        n = len(rows) if outline == 'all' else int(outline)
        for d, c in rows[:n]:
            print('%s%-3d %-18s %s  %s' % ('  ' * d, d, c['speaker'][:18], c['when'], c['text'][:76]))


if __name__ == '__main__':
    main()
