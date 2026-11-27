#!/usr/bin/env bash
# scan_pairip.sh [serial] - which apps on this device gate startup on Google Play?
#
# Two manifest shapes exist, and they need different patches:
#
#   APPLICATION  <application android:name="com.pairip.application.Application">
#                repoint that attribute at the app's own Application class
#                (find it with: apktool d -r, then grep -B4
#                 '^\.super Landroid/app/Application;')
#   PROVIDER     declares com.pairip.licensecheck.LicenseContentProvider
#                delete that <provider> element with axml_remove_element.py
#   dormant      PairIP classes are present but nothing is declared/called;
#                no patch needed
#   native=yes   libpairipcore.so ships in the APK: PairIP's VM protects the
#                dex, so manifest edits crash it - leave the Play build alone
#
# Run after every app update; patch only rows that are APPLICATION or PROVIDER.
set -uo pipefail

DIR=$(cd "$(dirname "$0")" && pwd)
SER=${1:-$(adb devices | awk '/\tdevice$/{print $1; exit}')}
[ -n "$SER" ] || { echo "no device" >&2; exit 1; }

WORK=$(mktemp -d "${TMPDIR:-/tmp}/pairip.XXXXXX")
trap 'rm -rf "$WORK"' EXIT

# Collect one manifest per third-party app that mentions pairip at all.
adb -s "$SER" shell sh -s <<'EOF'
rm -rf /data/local/tmp/.pairip && mkdir -p /data/local/tmp/.pairip
for p in $(pm list packages -3 | sed 's/^package://'); do
  base=$(pm path "$p" | sed -n '1s/^package://p')
  [ -z "$base" ] && continue
  unzip -p "$base" AndroidManifest.xml > /data/local/tmp/.pairip/.m.xml 2>/dev/null || continue
  tr -d '\000' < /data/local/tmp/.pairip/.m.xml | grep -q 'com\.pairip' || continue
  mv /data/local/tmp/.pairip/.m.xml "/data/local/tmp/.pairip/$p.xml"
done
EOF

adb -s "$SER" pull /data/local/tmp/.pairip "$WORK/" >/dev/null 2>&1
adb -s "$SER" shell rm -rf /data/local/tmp/.pairip

printf '%-45s %-11s %s\n' package gate native
printf '%-45s %-11s %s\n' ------- ---- ------
for f in "$WORK"/.pairip/*.xml; do
  [ -e "$f" ] || continue
  pkg=$(basename "$f" .xml)
  line=$(python3 "$DIR/axml_scan.py" "$f" 2>/dev/null) || { echo "$pkg  unparsable"; continue; }
  app=$(sed -n 's/.*app=\([^ ]*\) providers=.*/\1/p' <<<"$line")
  prov=$(sed -n 's/.*providers=\([^ ]*\) activities=.*/\1/p' <<<"$line")
  case "$app" in
    com.pairip.*) gate=APPLICATION ;;
    *) case "$prov" in
         -) case "$line" in *activities=com.pairip*) gate=dormant ;; *) gate=unknown ;; esac ;;
         *) gate=PROVIDER ;;
       esac ;;
  esac
  nat=no
  n=$(adb -s "$SER" shell "pm path $pkg | sed 's/^package://' | while read -r a; do unzip -l \"\$a\" 2>/dev/null; done | grep -c libpairipcore" 2>/dev/null | tr -d '\r')
  [ "${n:-0}" != "0" ] && nat=yes
  printf '%-45s %-11s %s\n' "$pkg" "$gate" "$nat"
done
