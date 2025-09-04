### Lessons Learned: Interacting with Android Apps via `am`

1.  **Basic URL Launching:** The most reliable way to open a URL in the default browser is using a generic `VIEW` intent:
    *   `am start -a android.intent.action.VIEW -d <URL>`
    *   This works without special permissions as it relies on the system's default app handling.

2.  **Targeting Specific Activities (Package/Activity Name):**
    *   `am start -n <package_name>/<activity_name>`
    *   This method is effective for activities explicitly marked as `exported="true"` in the app's `AndroidManifest.xml`.
    *   **On Rooted Devices with `sudo`**: Even for activities not explicitly exported (e.g., `org.chromium.chrome.browser.settings.SettingsActivity`, `org.chromium.chrome.browser.customtabs.CustomTabActivity`, `com.google.android.apps.chrome.TranslateDispatcher`), using `sudo am start` can *visually succeed* in launching the activity and displaying content, despite the shell reporting `SecurityException` or non-zero exit codes. This indicates that `sudo` bypasses the calling process's permission limitations, allowing the Android system to process the intent.

3.  **Deep Links (`chrome://` URLs):**
    *   `am start -n <package_name>/<main_activity> -a android.intent.action.VIEW -d "chrome://<path>"`
    *   This is a powerful way to access internal browser pages (like settings or extensions) that might not have directly callable activities. It leverages the browser's own URL handling.

4.  **Interacting with Services:**
    *   `am startservice -n <package_name>/<service_name>`
    *   Similar to activities, services must be `exported="true"` or require specific permissions. On a rooted device, `sudo` might still not bypass these explicit export restrictions if the service is not designed for external calls.

5.  **Sending Broadcasts:**
    *   `am broadcast -a <action> -n <package_name>/<receiver_name>`
    *   This can be successful if the receiver is exported or the calling app has the necessary permissions (e.g., `com.google.android.c2dm.intent.RECEIVE` broadcast to `FirebaseInstanceIdReceiver`).

6.  **Querying Content Providers:**
    *   `content query --uri content://<authority>/<path>`
    *   Accessing content providers often requires specific permissions (e.g., `android.permission.ACCESS_CONTENT_PROVIDERS_EXTERNALLY`). Even with `sudo`, environment-specific linker errors can occur, preventing successful execution.

### How to Find Activities and Services for Any Android App

To effectively interact with an Android application, you need to know its package name and the names of its components (activities, services, receivers, providers). Here's the process:

1.  **Find the Package Name:**
    *   Use `pm list packages` to list all installed packages. You can filter the output using `grep`:
        `pm list packages | grep -i <app_name_keyword>`
        (e.g., `pm list packages | grep -i kiwi` to find `com.kiwibrowser.browser`)

2.  **Get the APK Path:**
    *   Once you have the package name, use `pm path` to find the installation path of its APK file(s):
        `pm path <package_name>`
        (e.g., `pm path com.kiwibrowser.browser`)
    *   This will typically return paths like `/data/app/.../base.apk`.

3.  **Dump `AndroidManifest.xml` for Component Details:**
    *   The `AndroidManifest.xml` file within the APK declares all activities, services, receivers, and content providers, along with their intent filters and `exported` status. You can extract this information using `aapt` (Android Asset Packaging Tool), which is usually available in Termux after installing `aapt` or `android-tools`:
        `aapt dump xmltree <path_to_base.apk> AndroidManifest.xml`
        (e.g., `aapt dump xmltree /data/app/~~yUhZKFObQFUxvqi0lqrSFg==/com.kiwibrowser.browser-A3CGaj2k4qsIg3B7CXNF-w==/base.apk AndroidManifest.xml`)
    *   Look for `<activity>`, `<service>`, `<receiver>`, and `<provider>` tags.
    *   Pay close attention to the `android:name` attribute (which gives the full class name) and the `android:exported` attribute (which indicates if it can be launched by other apps). Also, examine nested `<intent-filter>` tags to understand what actions and data types a component can handle.

4.  **Use `dumpsys package` for Runtime Information (Requires `sudo` on rooted devices):**
    *   `sudo dumpsys package <package_name>`
    *   This command provides a very detailed runtime state of the package. **It requires `sudo` because `dumpsys` needs root privileges (UID 0) to access system-level information about other applications.** Termux runs as a standard user application and does not have these permissions by default. Without `sudo`, you will get a `Permission Denial` error.
    *   The output includes:
        *   Resolved intent filters for activities and services.
        *   Declared and requested permissions.
        *   Granted permissions.
        *   **Enabled/Disabled components**: This is crucial, as a component might be declared in `AndroidManifest.xml` but disabled at runtime, preventing its launch. (e.g., `org.chromium.chrome.browser.media.AudioLauncherActivity` was listed as `disabledComponents` in our test).

By combining these methods, you can gain a comprehensive understanding of an Android application's exposed and internal components, allowing for more targeted and informed `am` commands.