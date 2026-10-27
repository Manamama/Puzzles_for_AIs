#!/usr/bin/env python3
"""Replace one string value inside a binary AndroidManifest.xml (AXML).

Rebuilds the UTF-16 string pool (same string count, so all indices stay valid),
shifts the remaining chunks and fixes the root chunk size. No other semantics change.
"""
import struct, sys


def read_pool(buf, off):
    _typ, _hsz, size = struct.unpack_from('<HHI', buf, off)
    sc, stc, flags, sstart, ststart = struct.unpack_from('<IIIII', buf, off + 8)
    if flags & 0x100:
        raise SystemExit('UTF-8 pool not supported by this patcher')
    if stc:
        raise SystemExit('styled pool not supported')
    offs = list(struct.unpack_from('<%dI' % sc, buf, off + 28))
    strings = []
    for o in offs:
        p = off + sstart + o
        n = struct.unpack_from('<H', buf, p)[0]
        p += 2
        if n & 0x8000:
            n = ((n & 0x7fff) << 16) | struct.unpack_from('<H', buf, p)[0]
            p += 2
        strings.append(buf[p:p + n * 2].decode('utf-16-le'))
    return strings, off + size


def build_pool(strings):
    data = bytearray()
    offs = []
    for s in strings:
        offs.append(len(data))
        raw = s.encode('utf-16-le')
        n = len(raw) // 2
        if n > 0x7fff:
            data += struct.pack('<H', 0x8000 | (n >> 16)) + struct.pack('<H', n & 0xffff)
        else:
            data += struct.pack('<H', n)
        data += raw
        data += b'\x00\x00'
    while len(data) % 4:
        data += b'\x00'
    header_size = 28
    strings_start = header_size + 4 * len(strings)
    chunk = struct.pack('<HHI', 0x0001, header_size, strings_start + len(data))
    chunk += struct.pack('<IIIII', len(strings), 0, 0, strings_start, 0)
    chunk += struct.pack('<%dI' % len(strings), *offs)
    return chunk + bytes(data)


def patch(path, old, new, out):
    buf = open(path, 'rb').read()
    typ, hsz, size = struct.unpack_from('<HHI', buf, 0)
    if typ != 0x0003:
        raise SystemExit('not an AXML file')
    if size != len(buf):
        print('warning: root size %d != file size %d' % (size, len(buf)))
    strings, after_pool = read_pool(buf, 8)
    hits = [i for i, s in enumerate(strings) if s == old]
    if len(hits) != 1:
        raise SystemExit('expected exactly one %r, found %d' % (old, len(hits)))
    strings[hits[0]] = new
    new_pool = build_pool(strings)
    old_pool = buf[8:after_pool]
    delta = len(new_pool) - len(old_pool)
    out_buf = bytearray(buf[:8] + new_pool + buf[after_pool:])
    struct.pack_into('<I', out_buf, 4, len(out_buf))
    open(out, 'wb').write(out_buf)
    print('patched string #%d: %r -> %r; pool %d -> %d bytes, file %d -> %d (delta %+d)'
          % (hits[0], old, new, len(old_pool), len(new_pool), len(buf), len(out_buf), delta))


if __name__ == '__main__':
    patch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
