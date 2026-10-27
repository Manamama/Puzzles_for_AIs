#!/usr/bin/env python3
"""Rebuild an APK with a replaced AndroidManifest.xml, writing an aligned ZIP.

Alignment rules (same intent as `zipalign -p 4`):
  * *.so (stored)      -> 4096-byte page alignment (mmap loader)
  * any stored entry   -> 4-byte alignment (resources.arsc)
  * deflated entries   -> no alignment needed

Padding is carried in the 0xd935 "Android ZIP alignment" extra field, which
Android ignores. Entries keep their original order, timestamps and attributes.
"""
import struct
import sys
import zipfile
import zlib

ALIGN_EXTRA_ID = 0xD935


def _dos_time_date(dt):
    y, mo, d, h, mi, s = dt
    if y < 1980:
        y = 1980
    return (h << 11) | (mi << 5) | (s // 2), ((y - 1980) << 9) | (mo << 5) | d


def _extra_for(base_len, align):
    if align <= 1:
        return b''
    # extra field = 4-byte header + 2-byte alignment value + padding
    pad = (align - ((base_len + 6) % align)) % align
    payload = struct.pack('<H', align) + b'\x00' * pad
    return struct.pack('<HH', ALIGN_EXTRA_ID, len(payload)) + payload


def build(src, manifest_bytes, out_path):
    with zipfile.ZipFile(src) as zin:
        members = []
        for info in zin.infolist():
            if info.filename.startswith('META-INF/') and (
                    info.filename == 'META-INF/MANIFEST.MF'
                    or info.filename.upper().endswith(('.SF', '.RSA', '.DSA', '.EC'))):
                continue
            data = zin.read(info.filename)
            if info.filename == 'AndroidManifest.xml':
                data = manifest_bytes
            members.append((info, data))

    out = bytearray()
    central = []
    central_extra = {}
    for info, data in members:
        name = info.filename.encode('utf-8')
        utf8_flag = 0x800 if any(b > 0x7F for b in name) else 0x0
        if info.compress_type == zipfile.ZIP_DEFLATED:
            co = zlib.compressobj(9, zlib.DEFLATED, -15)
            comp = co.compress(data) + co.flush()
            method = 8
        else:
            comp = data
            method = 0
        crc = zlib.crc32(data) & 0xFFFFFFFF
        dtime, ddate = _dos_time_date(info.date_time)

        if method == 0:
            align = 4096 if info.filename.endswith('.so') else 4
        else:
            align = 1
        extra = _extra_for(len(out) + 30 + len(name), align)
        offset = len(out)

        out += struct.pack('<IHHHHHIIIHH', 0x04034B50, 20, utf8_flag, method,
                           dtime, ddate, crc, len(comp), len(data), len(name), len(extra))
        out += name + extra + comp
        central_extra[(name, offset)] = extra
        central.append((name, utf8_flag, method, dtime, ddate, crc, len(comp),
                        len(data), offset, info.external_attr))

    cd_start = len(out)
    for (name, flags, method, dtime, ddate, crc, csize, usize,
         offset, ext_attr) in central:
        extra = central_extra[(name, offset)]
        out += struct.pack('<IHHHHHHIIIHHHHHII', 0x02014B50, 20, 20, flags, method,
                           dtime, ddate, crc, csize, usize, len(name), len(extra), 0, 0, 0,
                           ext_attr, offset)
        out += name + extra
    cd_size = len(out) - cd_start
    out += struct.pack('<IHHHHIIH', 0x06054B50, 0, 0, len(central), len(central),
                       cd_size, cd_start, 0)

    with open(out_path, 'wb') as fh:
        fh.write(out)
    print('wrote %s: %d entries, %d bytes' % (out_path, len(central), len(out)))

    # report alignment of the entries that matter
    with zipfile.ZipFile(out_path) as z:
        for info in z.infolist():
            if info.filename in ('resources.arsc', 'AndroidManifest.xml'):
                off = info.header_offset + 30 + len(info.filename.encode()) + len(info.extra)
                print('  %-22s data_offset=%d (mod4=%d)' % (info.filename, off, off % 4))


if __name__ == '__main__':
    build(sys.argv[1], open(sys.argv[2], 'rb').read(), sys.argv[3])
