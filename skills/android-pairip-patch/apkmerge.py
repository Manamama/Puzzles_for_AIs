#!/usr/bin/env python3
"""Merge split APKs into a base APK, so a plain single-APK install works.

  apkmerge.py base.apk out.apk split.apk [split.apk ...]

Why: a split-only app installed as one file dies with INSTALL_FAILED_MISSING_SPLIT.
Where the target device gives you no privileged shell (no adb, no rish/Shizuku, no
su) a session install is impossible and a single tappable APK is the only route.

What it copies from each split: every entry except AndroidManifest.xml and
stamp-cert-sha256. For an ABI split that is lib/…/libfoo.so, which is the only
part the app cannot run without. Resource splits (locale, density) may be merged
the same way or simply left out — Android falls back to base resources.

Afterwards the manifest still has to stop demanding splits: remove the
`com.android.vending.splits.required` meta-data (axml_remove_element.py) and
empty `android:requiredSplitTypes` (axml_patch.py), then repack with
apkbuild.py, which stores *.so and page-aligns it for extractNativeLibs="false".
"""
import sys
import zipfile

SKIP = {'AndroidManifest.xml', 'stamp-cert-sha256'}


def merge(base, out_path, splits):
    added = []
    with zipfile.ZipFile(base) as src, zipfile.ZipFile(out_path, 'w') as out:
        for i in src.infolist():
            ni = zipfile.ZipInfo(i.filename, i.date_time)
            ni.compress_type = i.compress_type
            ni.external_attr = i.external_attr
            out.writestr(ni, src.read(i.filename))
        for path in splits:
            with zipfile.ZipFile(path) as sp:
                for i in sp.infolist():
                    if i.filename in SKIP:
                        continue
                    ni = zipfile.ZipInfo(i.filename, i.date_time)
                    ni.compress_type = i.compress_type
                    ni.external_attr = i.external_attr
                    out.writestr(ni, sp.read(i.filename))
                    added.append(i.filename)
    with zipfile.ZipFile(out_path) as z:
        print('wrote %s: %d entries' % (out_path, len(z.infolist())))
    for a in added:
        print('  + %s' % a)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    merge(sys.argv[1], sys.argv[2], sys.argv[3:])
