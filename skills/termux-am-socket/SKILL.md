# Termux-AM Socket: Skill Guide for AI Systems

## Overview

`termux-am` is a fast, socket-based interface for executing Android Activity Manager (`am`) commands from within Termux without spawning a Dalvik VM. It's roughly **10x faster** than the traditional `am` command because it reuses the Termux app's Java process instead of creating a new one each time.

**Key Points:**
- Uses Unix Domain Socket (IPC, not network)
- No root required
- ~10x faster than spawning `am` via Dalvik VM
- Available in Termux by default (enabled by default in `termux.properties`)
- Only accessible by termux user and root user

---

## Architecture

### Socket Path
```
/data/data/com.termux/files/apps/com.termux/termux-am/am.sock
```

### How It Works

1. **Client** (termux-am CLI tool) converts shell arguments using `bash printf "%q"` quoting
2. **Client** connects to Unix domain socket at the path above
3. **Server** (TermuxAmSocketServer running inside Termux app) receives the string
4. **Server** executes the am command via Android Java API (no VM spawn)
5. **Server** sends back stdout, stderr, and exit code
6. **Client** displays results and exits

### Why It's Fast

```
Traditional am:
  bash → spawn Dalvik VM → execute am → load Java runtime → run command → exit VM
  Time: 200-500ms per command

termux-am socket:
  bash → connect socket → send string → reuse app process → run command → return
  Time: 20-50ms per command
```

---

## Protocol Specification

### Simple String-Based Protocol

The protocol is deliberately simple for compatibility:

#### Client → Server Message
```
<argument_string>
```

Where `<argument_string>` is:
- The arguments converted to a single quoted string using bash `printf "%q"`
- Example: `"start-server"` or `"start-activity -n com.example.app/.MainActivity"`
- Sent as null-terminated or complete message via Unix socket

#### Server → Client Response
```
<stdout_data>\0
<stderr_data>\0
<exit_code_as_string>
```

Example response for successful command:
```
List of devices attached\n...\0\0
0
```

### Implementation Notes

The termux-am wrapper script uses bash's `printf "%q"` built-in to convert the arguments array into a properly quoted single string that can be reused as shell input.

**Why this matters for AI:**
- The socket server expects shell-escaped strings
- Special characters, spaces, and quotes must be properly escaped using shell quoting rules
- This is why the wrapper script exists—it handles the escaping automatically

---

## Usage Examples

### Via Command Line (termux-am wrapper)

```bash
# List connected devices
termux-am am device-id

# Start an activity
termux-am am start -n com.example.app/.MainActivity

# Send broadcast
termux-am am broadcast -a android.intent.action.BOOT_COMPLETED

# Kill a process
termux-am am kill-all com.example.app

# Get device properties
termux-am am get-prop ro.build.version.release
```

### Direct Socket Access (Advanced)

If writing in Python, C, or other languages, you would:

```python
import socket
import os

socket_path = "/data/data/com.termux/files/apps/com.termux/termux-am/am.sock"

# Connect to socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(socket_path)

# Send command (must be shell-quoted)
command = 'am device-id'  # Already quoted by shell
sock.sendall(command.encode() + b'\0')

# Receive response
stdout = b""
while True:
    chunk = sock.recv(4096)
    if not chunk:
        break
    stdout += chunk

sock.close()
```

---

## When to Use termux-am (Performance-Critical Scenarios)

### Good Use Cases

1. **Rapid polling** - Check device state repeatedly
   ```bash
   # Instead of: for i in {1..100}; do am device-id; done  [10+ seconds]
   # Use: termux-am in a loop                                [<1 second]
   ```

2. **Scripted automation** - Automate many Android operations
   ```bash
   for app in com.app1 com.app2 com.app3; do
     termux-am am force-stop $app
   done
   ```

3. **Real-time monitoring** - Watch device state
   ```bash
   while true; do
     termux-am am get-config > config.txt
     sleep 1
   done
   ```

4. **Termux:API integration** - Send commands to Termux app
   ```bash
   termux-am am send-notification --id 1 "Title" "Message"
   ```

### Bad Use Cases

1. **One-off commands** - Performance gain is negligible
2. **Complex am operations** that need interactive shells

---

## Compatibility & Configuration

### Checking if Socket Server is Enabled

```bash
echo $TERMUX_APP__AM_SOCKET_SERVER_ENABLED
# Output: (empty or true)
```

If output is `false`, socket server is disabled.

### Enabling/Disabling Socket Server

Add to `~/.termux/termux.properties`:

```properties
run-termux-am-socket-server=true   # Enable (default)
# or
run-termux-am-socket-server=false  # Disable
```

Then restart Termux app.

### Fallback Behavior

Modern `termux-am` automatically:
1. Tries to connect to socket
2. Falls back to spawning `am` if socket is unavailable
3. Returns same output format either way

This means scripts don't need to worry about which method is being used.

---

## Commands Available via termux-am

All standard Android `am` commands are available:

### Activity Management
- `start <INTENT>` - Start activity
- `startservice <INTENT>` - Start service
- `broadcast <INTENT>` - Send broadcast
- `instrument` - Run instrumentation

### Process Management
- `kill <PID>` - Kill process by ID
- `kill-all <PACKAGE>` - Kill all processes of package
- `force-stop <PACKAGE>` - Force stop package

### Device Information
- `device-id` - Get device serial
- `get-config` - Get current configuration
- `get-prop <PROPERTY>` - Get system property

### Stack Management
- `stack start` - Start activity stack
- `stack move-task` - Move task in stack

See `termux-am am --am-help` for complete list.

---

## Integration with Local AI (e.g., Gemini CLI)

### How an AI Should Use termux-am

When a local AI model needs to execute Android commands:

1. **Always use termux-am**, not bare `am`, because:
   - Consistent interface across devices
   - ~10x faster (important for tight loops)
   - Available in Termux environment

2. **Proper quoting** - Use shell escaping for complex args:
   ```bash
   # Correct:
   termux-am am broadcast -a android.intent.action.SEND --es text "Hello World"
   
   # Wrong (will fail):
   termux-am am broadcast -a android.intent.action.SEND --es text Hello World
   ```

3. **Error handling** - Check exit codes:
   ```bash
   termux-am am force-stop com.example.app
   if [ $? -eq 0 ]; then
     echo "Success"
   else
     echo "Failed"
   fi
   ```

4. **Parsing output** - Standard format:
   ```bash
   DEVICE_ID=$(termux-am am device-id)
   echo "Device: $DEVICE_ID"
   ```

### Example: Scripting with termux-am

```bash
#!/bin/bash
# Script to monitor and restart failed apps

APPS=("com.example.app1" "com.example.app2")
SOCKET="/data/data/com.termux/files/apps/com.termux/termux-am/am.sock"

while true; do
  for app in "${APPS[@]}"; do
    # Check if app is running (using termux-am for speed)
    if ! termux-am am pidof $app > /dev/null 2>&1; then
      echo "[$app] Not running, restarting..."
      termux-am am start -n $app/.MainActivity
    fi
  done
  sleep 5
done
```

---

## Troubleshooting

### "Could not connect to socket: No such file or directory"

**Cause**: Socket server not running

**Solution**:
```bash
# Check if enabled
cat ~/.termux/termux.properties | grep am-socket

# If not present or false, add:
echo "run-termux-am-socket-server=true" >> ~/.termux/termux.properties

# Restart Termux app completely
```

### Socket Exists but Commands Fail

**Cause**: Wrong socket path or permissions

**Solution**:
```bash
# Verify socket exists
ls -la /data/data/com.termux/files/apps/com.termux/termux-am/am.sock

# Check Termux version
termux-am --version

# Try fallback to regular am
am device-id
```

### Performance Still Slow

**Cause**: May be using fallback (spawning Dalvik VM)

**Solution**:
```bash
# Enable debug output
ADB_TRACE=all termux-am am device-id 2>&1 | grep socket

# This shows whether socket connection succeeded
```

---

## References

- **Source**: https://github.com/termux/termux-am-socket
- **Socket Server**: https://github.com/termux/termux-app (TermuxAmSocketServer.java)
- **Protocol Details**: termux-am-socket/termux-am.cpp
- **Termux Docs**: https://wiki.termux.com/wiki/Termux-am

---

## Summary for AI Implementations

**Key Behaviors to Implement:**

1. **Always prefer `termux-am` over `am`** in Termux environments
2. **Handle socket failures gracefully** (fallback to am)
3. **Understand the 10x speedup** applies mainly to batch operations
4. **Parse output correctly** (stdout, stderr, exit code)
5. **Use proper shell quoting** for complex arguments
6. **Cache socket connection** if making many rapid calls (don't reconnect each time)
7. **Document termux-am usage** in any tool that automates Android operations from Termux

**For Prompt Engineering:**

When instructing a local AI to use termux-am:

```
"Use termux-am instead of am for Android commands when in Termux. 
The socket-based approach is ~10x faster. Ensure proper shell quoting 
for complex arguments. Handle socket connection failures by falling back 
to regular am. Parse stdout, stderr, and exit codes from responses."
```
