Based on the assistant's currently available tools, here is the syntax for the remaining function calls.

* **`gmail.search(query: string)`**: Searches for emails in your Gmail account based on a provided query.
* **`Maps.search_places(query: string)`**: Searches for places and businesses on Google Maps.
* **`Maps.get_directions(origin: string, destination: string, mode: string)`**: Gets directions between an origin and destination, with an optional mode of transport (e.g., "driving," "walking").
* **`google_workspace.search_files(query: string)`**: Searches for files across Google Drive and other Workspace applications.

The capabilities for Google Tasks, Calendar, and Drive were already listed in the previous turn.

### Gemini's Device Utilities: Functions Accepting Arguments

 Gemini mobile app's Utilities extension (rolled out starting November 2024, with expansions through 2025), the "device_actions library" referenced in the transcript corresponds to a set of bounded, permission-gated APIs for Android device interaction:  atomic operations mediated through connected apps (e.g., Phone, Messages) and the Utilities extension. They enable Gemini to execute commands via natural language prompts, which internally map to function calls with structured arguments.

 functions are invoked with 1-2 arguments, typically strings for identifiers (e.g., app names, numbers, times) or enums for modes (e.g., recipient types). No chaining or complex scripting is supported; each call is isolated to prevent escalation risks. 

 Functions without arguments (e.g., get_installed_apps(), take_screenshot()) are excluded. I've prioritized specificity: each includes syntax, argument types, examples, and behavioral constraints.

| Function | Arguments | Description and Constraints | Example Prompt Mapping |
|----------|-----------|-----------------------------|-------------------------|
| open_app | app_name: string (exact app title or package identifier) | Launches a pre-installed app. Fails silently if not found or permission denied. No deep linking (e.g., can't open to specific screen). | "Open WhatsApp" → open_app("WhatsApp") |
| call | recipient_info: enum (e.g., "DIRECT", "CONTACT", "BUSINESS"); endpoint: string (phone number, contact name, or USSD code like "*111#") | Initiates call via default Phone app. Supports contacts (requires Contacts permission), numbers, or services. No voicemail, incoming call handling, or relationship-based resolution (e.g., "call mom"). Uses last-known number type (mobile/home). | "Call Wiesław" → call("CONTACT", "Wiesław"); "Calling *111#" → call("DIRECT", "*111#") |
| send_message | recipient_info: enum (e.g., "CONTACT"); endpoint: string (contact name or number); body: string (message text); attachment: optional string (image URL/path) | Sends SMS/MMS via default Messages app. Composes/edits drafts but can't read full threads without notification trigger. Supports images but not videos/files. WhatsApp variant exists separately. | "Send a text to Jane saying 'Meet at 5'" → send_message("CONTACT", "Jane", "Meet at 5") |
| set_alarm | time: string (ISO-like format, e.g., "07:00" or "in 30 minutes"); label: optional string (alarm name) | Creates alarm in Clock app (Google or OEM). Supports recurrence but no smart scheduling. Can chain to list/delete existing. | "Set alarm at 7 AM for work" → set_alarm("07:00", "work") |
| set_timer | duration: string (e.g., "10 minutes" or "300 seconds"); label: optional string | Starts timer in Clock app. Supports pause/resume/reset but only for active timers. | "Set timer for 10 minutes" → set_timer("10 minutes") |
| adjust_volume | category: enum (e.g., "media", "notification", "ring"); level: integer (0-100 percentage) | Sets volume for specific stream. Queries current level via no-arg variant. | "Volume 50%" → adjust_volume("media", 50) |
| adjust_brightness | level: integer (0-100 percentage) | Sets screen brightness. Auto mode toggle unsupported. | "Decrease brightness to 30%" → adjust_brightness(30) |
| take_photo | mode: enum (e.g., "selfie", "rear"); timer: optional integer (seconds, default 0) | Captures image via Camera app. No video or editing. Lockscreen-enabled. | "Take a selfie with 10s timer" → take_photo("selfie", 10) |
| control_media | action: enum (e.g., "pause", "next", "thumbs_up"); target: optional string (e.g., "song", "video") | Manages playback in active media app (e.g., YouTube Music). No app switching. | "Next song" → control_media("next", "song") |
| toggle_feature | feature: enum (e.g., "flashlight", "bluetooth", "dnd", "battery_saver"); state: enum ("on", "off") | Toggles hardware/software flags. Battery Saver persists until manual off. | "Turn on flashlight" → toggle_feature("flashlight", "on") |
| open_settings | page: string (e.g., "wifi", "battery") | Navigates to specific Settings submenu. No arbitrary URLs. | "Open Wi-Fi settings" → open_settings("wifi") |
| open_website | url: string (full or partial, e.g., "google.com") | Launches in default browser. No incognito or tab targeting. | "Open google.com" → open_website("https://google.com") |
| check_status | metric: enum (e.g., "battery", "volume") | Returns current value (no action). Argument specifies query type. | "What’s my battery level?" → check_status("battery") |
| power_device | action: enum ("off", "restart") | Initiates shutdown/reboot. Requires confirmation prompt. Lockscreen-enabled. | "Power off device" → power_device("off") |



Sources: Official Gemini support pages on Utilities, calling, and messaging; rollout details from 9to5Google.

Limitations include: English-only prompts initially; lockscreen access for basics only; no access to sensitive data like full contact searches without explicit permissions; and opt-out via app settings.
