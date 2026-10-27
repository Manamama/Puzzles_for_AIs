#!/usr/bin/env python3
"""Remove one element (start + end chunk) from a binary AndroidManifest.xml.

  axml_remove_element.py in.xml out.xml <element-name> <android:name-value>

The string pool, resource map and every other chunk are left byte-identical.
Only the element's START_ELEMENT..END_ELEMENT range is cut out and the root
chunk sizes are corrected.

Used for PairIP builds that gate startup through a ContentProvider instead of
the Application class: deleting that <provider> means Android never constructs
the licence client at all.
"""
import struct
import sys

START_ELEMENT = 0x0102
END_ELEMENT = 0x0103
ANDROID_NS = 'http://schemas.android.com/apk/res/android'


def read_pool(buf):
    typ, hsz, size = struct.unpack_from('<HHI', buf, 8)
    sc, stc, flags, sstart, _ststart = struct.unpack_from('<IIIII', buf, 16)
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


def node_name(buf, strings, off):
    return strings[struct.unpack_from('<I', buf, off + 20)[0]]


def android_name_value(buf, strings, off):
    """Return the android:name attribute value of a START_ELEMENT chunk."""
    attr_start, attr_size, attr_count = struct.unpack_from('<HHH', buf, off + 24)
    base = off + 16 + attr_start
    for i in range(attr_count):
        a = base + i * attr_size
        ns_idx, name_idx, raw_idx, _vsize, _res0, dtype, data = struct.unpack_from(
            '<IIIIHBB', buf, a)
        ns = strings[ns_idx] if ns_idx != 0xFFFFFFFF else ''
        if strings[name_idx] == 'name' and ns == ANDROID_NS:
            if dtype == 0x03:            # TYPE_STRING
                return strings[data]
            if raw_idx != 0xFFFFFFFF:
                return strings[raw_idx]
    return None


def chunks(buf):
    off = 8
    while off + 8 <= len(buf):
        typ, hsz, size = struct.unpack_from('<HHI', buf, off)
        if size == 0:
            break
        yield off, typ, size
        off += size


def remove(path, out_path, element, name_value):
    buf = open(path, 'rb').read()
    strings = read_pool(buf)
    target = None
    target_depth = -1
    depth = 0
    for off, typ, size in chunks(buf):
        if typ == START_ELEMENT:
            if target is None and node_name(buf, strings, off) == element \
                    and android_name_value(buf, strings, off) == name_value:
                target = off
                target_depth = depth
            depth += 1
        elif typ == END_ELEMENT:
            depth -= 1
            if target is not None and depth == target_depth:
                end = off + size
                break
    else:
        raise SystemExit('element %r/%r not found' % (element, name_value))
    if target is None:
        raise SystemExit('element %r with android:name=%r not found' % (element, name_value))
    new = bytearray(buf[:target] + buf[end:])
    struct.pack_into('<I', new, 4, len(new))          # whole-document size
    open(out_path, 'wb').write(new)
    print('removed <%s android:name=%r>: %d bytes -> %d' % (element, name_value, len(buf), len(new)))


if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    remove(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
