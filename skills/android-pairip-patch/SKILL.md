---
name: android-pairip-patch
description: Make Google Play–gated Android apps start on a device where Play licensing is unavailable or fails (Play Store disabled, de-Googled/Custom ROM, Magisk or rooted phone, emulator, sideloaded install, app not bought through Play). Diagnose PairIP (Play Automatic Integrity Protection) by shape — Application class, ContentProvider, or native VM — then patch the binary AndroidManifest.xml without apktool, rebuild and align the APK, re-sign base + splits with a local key, and reinstall over adb. Load when an app kills itself at startup and logcat mentions LicenseActivity, LicenseClient, or com.android.vending.licensing. Not for DRM video or banking apps.
---

# PairIP / Play-licensing startup gates — field procedure

An app that starts, flashes and closes on a device without working Play licensing is
usually not broken: it ran `com.pairip.licensecheck`, failed, and called `System.exit(0)`.
This skill removes the gate so the app runs. Aimed at apps you already own, on your own
device.

## 1. Confirm it is PairIP (30 seconds)

```bash
adb logcat -c
adb shell am start -W -n <pkg>/<pkg>.MainActivity
adb shell pidof <pkg>
adb logcat -d | grep -iE 'pairip|licens|FATAL EXCEPTION'
```

Signatures that it is PairIP and not a genuine crash:

```
LicenseClient: Retry #1. License check failed with error 'Could not bind with the
  licensing service: com.android.vending.licensing.ILicensingService'
ActivityManager: Unable to start service Intent { act=com.android.vending.licensing.ILicensingService
  pkg=com.android.vending } U=0: not found
ActivityTaskManager: START u0 {… com.pairip.licensecheck.LicenseActivity}
```

PairIP also fires on a **rooted** phone with a custom ROM or Magisk, even when the Play
Store is installed: the licence answer depends on Play's own integrity verdict, not on the
APK. Root does not fix it; re-signing does.

## 2. Triage all installed apps

```bash
bash scan_pairip.sh            # only connected device, or: bash scan_pairip.sh <serial>
```

```
package                       gate        native
flar2.devcheck                APPLICATION yes
com.simplecleanapp.gomoku…    PROVIDER    no
dev.opencode.mobile           dormant     no
```

| gate | meaning | action |
|---|---|---|
| `APPLICATION` | `<application android:name="com.pairip.application.Application">` | repoint to the app's own class |
| `PROVIDER` | declares `com.pairip.licensecheck.LicenseContentProvider` | delete that `<provider>` element |
| `dormant` | PairIP classes exist but nothing declares or calls them | nothing to do |
| `native=yes` | `libpairipcore.so` ships in the APK (PairIP's VM protects the dex) | **do not patch** — manifest edits crash inside the `.so`; keep the Play build |

Run the scan after every app update: a Play update silently reintroduces the gate.

## 3. The three shapes

**A. Application class.** Repoint the attribute at the class the app really uses. Find it:

```bash
apktool d -r -f -q base.apk -o x          # -r = skip resources, seconds instead of minutes
grep -rh -B4 '^\.super Landroid/app/Application;' x/smali*/ | grep '^\.class' | sed 's/.* L/L'
```

One hit is the real class (`Ldev/opencode/mobile/OpenCodeMobileApplication;` → drop `L`/`;`).
If the only hit is `Landroid/app/Application;` the app has no class of its own (typical
Flutter, or a small Compose app) → use `android.app.Application`.

**B. ContentProvider.** The provider is instantiated before any app code, and its
`onCreate()` builds a `LicenseClient` and calls `initializeLicenseCheck()`. There is no
caller in the app's dex — don't hunt for one. Delete the element.

**C. Native VM.** `libpairipcore.so` decrypts/verifies the dex at load; a patched manifest
makes the process abort inside the library (`F DEBUG … libpairipcore.so`). Out of scope
here. Note it and move on.

## 4. Procedure

```bash
P=dev.opencode.mobile                        # sample app names are real, kept on purpose
S=$HOME/android-pairip-patch                # or your date-stamped work dir
mkdir -p "$S"/{orig,work,signed}

# pull base + every split (splits carry native libs / locales / densities)
adb shell "pm path $P" | sed 's/^package://' | tr -d '\r' | while read -r f; do
  adb pull "$f" "$S/orig/$(basename "$f")"; done

# extract and patch the manifest — pick ONE:
python3 -c "import zipfile; zipfile.ZipFile('$S/orig/base.apk').extract('AndroidManifest.xml','$S/work')"

python3 axml_patch.py "$S/work/AndroidManifest.xml" \
  com.pairip.application.Application <real.class.Name> "$S/work/manifest.patched.xml"

# or, for a ContentProvider gate:
python3 axml_remove_element.py "$S/work/AndroidManifest.xml" \
  "$S/work/manifest.patched.xml" provider com.pairip.licensecheck.LicenseContentProvider

# rebuild base (copy every other entry untouched, fix alignment), sign base + splits
python3 apkbuild.py "$S/orig/base.apk" "$S/work/manifest.patched.xml" "$S/work/base-patched.apk"
KS=$HOME/patch.jks; KP=$HOME/patch.pass
apksigner sign --ks "$KS" --ks-key-alias <alias> --ks-pass "file:$KP" "$S/work/base-patched.apk"
for f in "$S"/orig/split_*.apk; do
  cp "$f" "$S/signed/"; apksigner sign --ks "$KS" --ks-key-alias <alias> \
    --ks-pass "file:$KP" "$S/signed/$(basename "$f")"; done

# same signing key on every split, or install fails / app crashes on missing split
adb uninstall "$P"                                        # signature changed ⇒ data loss
adb install-multiple "$S/work/base-patched.apk" "$S"/signed/split_*.apk
```

Verify exactly as in step 1: process alive, no `LicenseClient` lines, and the expected
activity is resumed:

```bash
adb shell dumpsys activity activities | grep -m1 ResumedActivity
```

## 5. Pitfalls that cost real attempts

- **The AXML string pool is UTF-16.** `grep -a pairip AndroidManifest.xml` finds nothing.
  Pipe through `tr -d '\000'` first (that is what `scan_pairip.sh` does on-device).
- **Removing an element leaves its strings in the pool**, so a text grep still reports
  `LicenseContentProvider` after a successful patch. Only a structural parse
  (`axml_scan.py`) tells the truth.
- **`apktool b` is often useless on Debian/Ubuntu**: the packaged aapt rejects modern
  resources (`First type is not attr!`, exit 134) on targetSdk 30+ apps. That is why
  patching is byte-level manifest surgery + `apkbuild.py`, not a resource rebuild.
- **Rebuild only the base.** Splits only need `apksigner`; it keeps their `.so` entries
  page-aligned. Rebuilding a split re-compresses it and buys nothing.
- **Alignment matters**: uncompressed `resources.arsc` 4-byte, stored `.so` 4 KiB.
  `apkbuild.py` carries padding in the `0xd935` extra field, same as `zipalign -p 4`.
- **`aapt2 dump` in Debian has no `--file`.** Use `aapt dump xmltree app.apk
  AndroidManifest.xml` (v1) for inspection.
- **Uninstall deletes app data.** After reinstalling, the app must be set up again
  (pairing, logins, game progress). Say so before doing it.
- **The app is frozen at that version**: Play/Aurora updates will be rejected because the
  signature no longer matches. Re-patch each new version.
- Do not touch a `native=yes` app. Its PairIP is in the dex cipher, not the manifest.

## 6. Rooted devices

Root does not remove the gate, but it changes the options:

- **Same pipeline.** adb is adb; a Magisk phone is patched identically (the RMX3085 /
  Android 11 case).
- **Keep signatures (no data loss)**: with root you can bind-mount or replace the patched
  APK into `/data/app/...` while keeping the original certificate. Fragile across app
  updates and Play re-verification; document it if you rely on it.
- **Runtime hook instead of re-signing**: an LSPosed/Xposed module that stubs
  `ILicensingService` lets Play updates keep flowing. Untested in this skill — treat as a
  direction, not a recipe.
- Do not weaken the device (disable verity, flash odd modules) to solve a licensing
  problem that lives in an APK.

## 7. Tool reference

| File | Purpose |
|---|---|
| `scan_pairip.sh` | device-wide triage; pulls manifests only, parses them structurally |
| `axml_scan.py` | one manifest → `app=… providers=… activities=… services=… receivers=…` |
| `axml_patch.py` | replace one string in a binary `AndroidManifest.xml` (same pool size) |
| `axml_remove_element.py` | delete one element (start+end chunk) and fix root chunk sizes |
| `apkbuild.py` | repack APK with a new manifest, correct alignment, original entry order |

Requirements: `adb`, `python3`, `apksigner` (build-tools), `aapt` for inspection,
`apktool` only for finding an Application class. No keystore ships here — create your own:

```bash
keytool -genkeypair -keystore patch.jks -alias patch -keyalg RSA -keysize 4096 \
  -validity 10000 -storepass "$(openssl rand -hex 12 > patch.pass; cat patch.pass)"
```

## 8. Worked cases (fixed sample names)

| App | Version | Shape | Patch |
|---|---|---|---|
| `dev.opencode.mobile` | 1.3.0 | Application | → `dev.opencode.mobile.OpenCodeMobileApplication` |
| `cc.agentlabs.opencode` | 0.4.15 | Application | → `cc.agentlabs.opencode.MainApplication` |
| `com.simplecleanapp.gomoku_five_in_a_row` | 1.0.25 | Provider | element removed |
| `pl.zenbytestudio.gomokuzen` | 0.0.2 | Provider | element removed |
| `com.basa.largetext` | 1.2.5 | Application | → `android.app.Application` (Flutter) |
| `flar2.devcheck` | — | native VM | left as Play build; its check never fires |

Pattern worth remembering: a Play **update** is what reintroduces the gate, and the same
app can change shape between versions — always rescan before patching, never reuse last
session's plan.
