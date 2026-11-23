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

Check what the app can actually reach before blaming root:

```bash
adb shell pm list packages -d | grep vending      # Play disabled ⇒ no ILicensingService
adb shell dumpsys package com.android.vending | grep enabled=
```

`enabled=3` (disabled) on a de-Googled or debloated phone is the whole story: the bind to
`com.android.vending.licensing.ILicensingService` fails with `not found`, so the gate fires
on *every* install, Play-bought or not. Root/Magisk is irrelevant to that; the manifest
patch is the fix.

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
Flutter, a small Compose app, or an SDL/C++ app) → use `android.app.Application`.

No apktool? In Termux it is one `apt install apktool` (3.0.3, aarch64) and `-r` decode of
a 5 MB APK takes ~7 s — worth it. If it is genuinely unavailable, read the dex string table
instead: every superclass is a type descriptor there.

```bash
unzip -p base.apk classes.dex | strings -a | grep -oE 'L[A-Za-z0-9/$_]*Application;' | sort -u
```

Exactly `Lcom/pairip/application/Application;` plus `Landroid/app/Application;` means the
same no-own-class case (`com.xojot.vrplayer` 2.6.3, SDL/C++ with a single
`lib/arm64-v8a/libnative-lib.so` in the ABI split).

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
adb shell "pm uninstall --user all $P"                     # signature changed ⇒ data loss
                                                           # --user all: clears stale records
adb install-multiple "$S/work/base-patched.apk" "$S"/signed/split_*.apk
```

Verify exactly as in step 1: process alive, no `LicenseClient` lines, and the expected
activity is resumed:

```bash
adb shell dumpsys activity activities | grep -m1 ResumedActivity
```

### 4a. No adb: when the target *is* this phone

`adb devices` empty is not a blocker. adb only supplies a **shell-uid** context; on a phone
that is also the analysis machine, reproduce it locally and skip `adbd`/`tcpip` entirely.

| need | use |
|---|---|
| `pm`, `am`, `cmd package`, `dumpsys`, `logcat`, `screencap` | `rish -c '<cmd>'` — exactly `adb shell` |
| read `/data/app/…`, chown, `restorecon`, staging | `sudo` (root) |

- **rish is shell uid, so it cannot read Termux `$HOME`** (0700, `u0_a278`). Stage the
  signed APKs in `/data/local/tmp/<dir>` — `sudo mkdir -p`, `chmod 755` dir, `chmod 644`
  files, so both shell and `system_server` can traverse it. Same reason never to install
  straight out of `$HOME`: `system_server` opens the file, and root-only access is not enough.
- Pull with `sudo cp /data/app/~~…/<pkg>-~~…/*.apk "$S/orig/"`, then
  `sudo chown -R $(id -u):$(id -g) "$S"` so the Termux-side tools can write results.
- `pm`/`am`/`cmd` are always present in `/system/bin`; root can run them, but the shell-uid
  route via `rish` matches the documented adb semantics most closely.
- **`pm install-multiple` does not exist on every ROM.** This one (realme RMX3085,
  Android 11) answers `Unknown command: install-multiple`; the package service is still
  complete, so use the session API with the **split names from the manifests**, not filenames:

  ```bash
  SID=$(rish -c 'cmd package install-create -r -t' | grep -oE '[0-9]+')
  rish -c "cmd package install-write $SID base.apk      /data/local/tmp/w/base-patched.apk"
  rish -c "cmd package install-write $SID config.arm64_v8a /data/local/tmp/w/split_config.arm64_v8a.apk"
  #   config.<name> = split='config.…' in aapt dump badging "$f"
  rish -c "cmd package install-commit $SID"
  ```

### 4b. No privileged shell at all → merge the splits, install one APK

A split-only app is uninstallable as a single file (`INSTALL_FAILED_MISSING_SPLIT`), and
`pm install`/session installs need `INSTALL_PACKAGES` — which an **app-uid** shell does not
have. When the target offers no adb, no working `rish`, and no `su` (AirNote: Magisk app
installed, **no `su` binary anywhere**, Shizuku server down, Android 10 so no wireless-debug
pairing), stop fighting for a privileged shell and build one self-contained APK.

```bash
# 1. stop the manifest demanding splits (start from the PairIP-patched manifest)
python3 axml_patch.py m.xml base__abi,base__density "" m2.xml      # empty requiredSplitTypes
python3 axml_remove_element.py m2.xml m3.xml meta-data com.android.vending.splits.required

# 2. merge the lib split into the base, then repack (stores + 4096-aligns *.so)
python3 apkmerge.py orig/base.apk work/merged.apk orig/split_config.arm64_v8a.apk
python3 apkbuild.py work/merged.apk m3.xml work/single.apk
apksigner sign --ks patch.jks --ks-key-alias patch \
  --ks-pass file:patch.pass --key-pass file:keypass.pass work/single.apk
```

- **Which splits can be dropped.** The ABI split is mandatory (`lib/…/libnative-lib.so`, the
  only native code in a C++/SDL app). Locale and density splits are resource tables only —
  omit them and Android falls back to base strings and bitmaps.
- Keep `extractNativeLibs="false"` **only if** the `.so` ends up stored and page-aligned;
  `apkbuild.py` does that. Otherwise flip it to `true`.
- Verify before shipping: `aapt dump xmltree single.apk AndroidManifest.xml | grep -i split`
  must show no `splits.required`, and the `.so` `data_offset % 4096 == 0`.
- Deploy from an app-uid shell with the GUI installer — that path is allowed without
  `INSTALL_PACKAGES`:
  `am start -a android.intent.action.VIEW -d file:///storage/emulated/0/Download/x.apk -t application/vnd.android.package-archive`
  Someone has to tap *Install*; an app uid cannot `dumpsys` or `screencap` to check.

## 5. Pitfalls that cost real attempts

- **The AXML string pool is UTF-16.** `grep -a pairip AndroidManifest.xml` finds nothing.
  Pipe through `tr -d '\000'` first (that is what `scan_pairip.sh` does on-device).
- **Removing an element leaves its strings in the pool**, so a text grep still reports
  `LicenseContentProvider` after a successful patch. Only a structural parse
  (`axml_scan.py`) tells the truth.
- **`apktool b` is often useless on Debian/Ubuntu**: the packaged aapt rejects modern
  resources (`First type is not attr!`, exit 134) on targetSdk 30+ apps. That is why
  patching is byte-level manifest surgery + `apkbuild.py`, not a resource rebuild.
  Termux 3.0.3 fails differently but just as early: `aapt2 compile --dir res` reports
  `error: resource 'drawable/$avd_hide_password__0' has invalid entry name` for the vector
  drawables apktool renames internally, and the build dies in ~17 s; `--use-aapt1e` no
  longer exists in 3.x (`b --help` offers only `--aapt <file>`). So apktool is a **decode
  tool only** — use it to find classes, never to rebuild.
- **Rebuild only the base.** Splits only need `apksigner`; it keeps their `.so` entries
  page-aligned. Rebuilding a split re-compresses it and buys nothing.
- **Alignment matters**: uncompressed `resources.arsc` 4-byte, stored `.so` 4 KiB.
  `apkbuild.py` carries padding in the `0xd935` extra field, same as `zipalign -p 4`.
- **`aapt2 dump` in Debian has no `--file`.** Use `aapt dump xmltree app.apk
  AndroidManifest.xml` (v1) for inspection.
- **`--ks-pass` and `--key-pass` must not name the same file.** apksigner reads each
  `file:` source as a stream and takes one password per request, so pointing both at
  `patch.pass` makes the second read return `end of file reached` and every sign fails
  (`IOException: Failed to read Key … password`). Use two files with the same value
  (`cp patch.pass keypass.pass`) or two lines in one file.
- **Uninstall deletes app data.** After reinstalling, the app must be set up again
  (pairing, logins, game progress). Say so before doing it — with root you can avoid it:
  `sudo tar -C /data/data -cf /data/local/tmp/p-data.tar <pkg>` before the uninstall, then
  after the install `sudo tar -C /data/data -xpf …`, `sudo chown -R $(sudo stat -c %u
  /data/data/<pkg>)` and `sudo restorecon -R /data/data/<pkg>`. The package name keys the
  data dir, so this survives the new signature; chown to whatever uid the reinstall got
  (identical here: `10637`), and skip it if the app migrated on first run.
- **`pm uninstall -k` (keep data) makes the next install impossible**: the retained data
  means PMS keeps the package identity, and `install-multiple` fails with
  `INSTALL_FAILED_UPDATE_INCOMPATIBLE … signatures do not match`. Plain `pm uninstall`
  can also leave a half-dead record (`dumpsys package` shows `pkg=null`, `pm path`
  returns nothing, `pm list packages -u` still lists it). **Use
  `pm uninstall --user all <pkg>`** — it cleared that record instantly, no reboot needed.
  Devices with a second user (realme's "App cloner" creates `User 11`) carry per-user
  records, which is how the `pkg=null` state happens in the first place.
- **Prove the patch is surgical** before blaming the tool for a crash: dump both manifests
  and diff them. `aapt dump xmltree base.apk AndroidManifest.xml` vs the patched APK; the
  only difference must be the patched attribute or the removed element (4–5 lines).
- **Cleared the gate ≠ working app.** Some apps die right after it, in their own code:
  `com.harmonynetwork.singsharp` 16.0.0 throws `AssertionError: couldn't initialize
  LocaleData for locale en` in Firebase Perf plus `FORTIFY: pthread_mutex_lock called on
  a destroyed mutex` → SIGABRT, with a 4-line manifest diff. Likely its own
  signature-derived key/anti-tamper. Report it as app-side; do not iterate on the manifest.
- **One app can declare two PairIP providers.** `com.chordai` 2.7.73 had
  `LicenseContentProvider` *and* `LicenseContentProvider1`; removing only the first is a
  silent no-op. `axml_scan.py` prints both — loop until `providers=-`.
- **The app is frozen at that version**: Play/Aurora updates will be rejected because the
  signature no longer matches. Re-patch each new version.
- Do not touch a `native=yes` app. Its PairIP is in the dex cipher, not the manifest.

## 6. Rooted devices

Root does not remove the gate, but it changes the options:

- **Same pipeline.** adb is adb; a Magisk phone is patched identically (the RMX3085 /
  Android 11 case). When the rooted phone is the one you are working on, root also replaces
  adb's shell context — see §4a: `rish` for shell uid, `sudo` for `/data/app` and staging.
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
| `apkmerge.py` | fold split APKs (lib/resources) into the base — one tappable APK for devices with no privileged shell |

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

realme RMX3085 (Android 11, Magisk 27, Play Store **disabled**), 2026-10-28:

| App | Version | Shape | Patch |
|---|---|---|---|
| `com.logicedge.opencodemobile` | 1.2.4 | Application | → `android.app.Application` |
| `dev.opencode.mobile` | 1.3.0 | Application | → `dev.opencode.mobile.OpenCodeMobileApplication` |
| `com.dolby.dolby234` | 1.10.1 | Application | → `com.dolby.sessions.DolbySessionsApplication` |
| `com.chordai` | 2.7.73 | Provider ×2 | both providers removed |
| `com.harmonynetwork.singsharp` | 16.0.0 | Provider | element removed; app then crashes in its own code |
| `com.xojot.vrplayer` | 2.6.3 | Application | → `android.app.Application` (SDL/C++, no own class); RMX3085: session install because its `pm` lacks `install-multiple`. AirNote (NoteAir, Android 10, no adb/root/rish): splits merged into one APK (§4b) — only a GUI tap can install there |

Pattern worth remembering: a Play **update** is what reintroduces the gate, and the same
app can change shape between versions — always rescan before patching, never reuse last
session's plan.
