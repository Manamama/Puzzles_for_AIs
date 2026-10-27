#!/usr/bin/env python3
"""Print the PairIP-relevant structure of a binary AndroidManifest.xml.

  axml_scan.py <AndroidManifest.xml>

Output (one line):
  app=<application android:name> providers=<pairip providers>
  activities=<pairip activities> services=... receivers=...

Unused strings left in the pool after a patch are ignored; only declared
elements are reported, so a patched manifest reads "app=android.app.Application"
with no pairip components.
"""
import struct
import sys

START_ELEMENT = 0x0102
ANDROID_NS = 'http://schemas.android.com/apk/res/android'


def read_pool(buf):
    flags = struct.unpack_from('<I', buf, 16 + 8)[0]
    sc, _stc, flags, sstart, _ = struct.unpack_from('<IIIII', buf, 16)
    if flags & 0x100:
        raise SystemExit('UTF-8 pool not supported')
    offs = struct.unpack_from('<%dI' % sc, buf, 8 + 28)
    strings = []
    for o in offs:
        p = 8 + sstart + o
        n = struct.unpack_from('<H', buf, p)[0]
        p += 2
        if n & 0x8000:
            n = ((n & 0x7fff) << 16) | struct.unpack_from('<H', buf, p)[0]
            p += 2
        strings.append(buf[p:p + n * 2].decode('utf-16-le'))
    return strings


def name_of(buf, strings, off):
    return strings[struct.unpack_from('<I', buf, off + 20)[0]]


def android_name(buf, strings, off):
    attr_start, attr_size, attr_count = struct.unpack_from('<HHH', buf, off + 24)
    base = off + 16 + attr_start
    for i in range(attr_count):
        a = base + i * attr_size
        ns_idx, name_idx, raw_idx, _vs, _r0, dtype, data = struct.unpack_from(
            '<IIIIHBB', buf, a)
        ns = strings[ns_idx] if ns_idx != 0xFFFFFFFF else ''
        if strings[name_idx] == 'name' and ns == ANDROID_NS:
            if dtype == 0x03:
                return strings[data]
            if raw_idx != 0xFFFFFFFF:
                return strings[raw_idx]
    return None


def main(path):
    buf = open(path, 'rb').read()
    strings = read_pool(buf)
    app = None
    found = {'provider': [], 'activity': [], 'service': [], 'receiver': []}
    depth = 0
    off = 8
    while off + 8 <= len(buf):
        typ, _hsz, size = struct.unpack_from('<HHI', buf, off)
        if typ == START_ELEMENT:
            el = name_of(buf, strings, off)
            n = android_name(buf, strings, off)
            if el == 'application' and depth == 1:
                app = n
            elif el in found and n and n.startswith('com.pairip'):
                found[el].append(n)
            depth += 1
        elif typ == 0x0103:                      # END_ELEMENT
            depth -= 1
        off += size
    print('app=%s providers=%s activities=%s services=%s receivers=%s' % (
        app or '<none>',
        ','.join(found['provider']) or '-',
        ','.join(found['activity']) or '-',
        ','.join(found['service']) or '-',
        ','.join(found['receiver']) or '-'))


if __name__ == '__main__':
    main(sys.argv[1])
