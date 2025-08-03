#!/bin/bash

# Function to find Droid IP (from memory)
find_droid_ip() {
    local gateway_ip=$(ip route | grep default | awk '{print $3}')
    local ip_prefix=$(echo "$gateway_ip" | cut -d'.' -f1-3)
    # Scan for port 8022 (SSH) as a reliable indicator of Droid presence
    local nmap_output=$(nmap -p 8022 "${ip_prefix}.0/24" | grep 'open' -B 4)
    local droid_ip=$(echo "$nmap_output" | grep -oP 'Nmap scan report for \K[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1)
    echo "$droid_ip"
}

# Get the Droid IP
DROID_IP=$(find_droid_ip)

if [ -z "$DROID_IP" ]; then
    echo "Error: Could not find Droid IP. Ensure Termux SSHD is running and device is on network." >&2
    exit 1
fi

# Termux user ID (common default)
TERMUX_UID="u0_a278"

# Termux environment variables
TERMUX_HOME="/data/data/com.termux/files/home"
TERMUX_PREFIX="/data/data/com.termux/files/usr"
# Comprehensive PATH including common Termux and Android system paths
TERMUX_PATH="${TERMUX_PREFIX}/bin:${TERMUX_PREFIX}/bin/applets:/system/bin:/system/xbin"
TERMUX_LD_LIBRARY_PATH="${TERMUX_PREFIX}/lib"

# The command to execute in Termux (all arguments passed to this script)
TERMUX_COMMAND_TO_RUN="$@"

# Construct the command string that su -c will execute on the Droid
# Use single quotes for robustness, escaping any internal single quotes as '\''
# The $PATH needs to be escaped for the remote shell
INNER_SU_COMMAND="export HOME=${TERMUX_HOME}; export PREFIX=${TERMUX_PREFIX}; export PATH=${TERMUX_PATH}:\$PATH; export LD_LIBRARY_PATH=${TERMUX_LD_LIBRARY_PATH}; ${TERMUX_COMMAND_TO_RUN}"

# The full adb shell command to execute locally
# Pass the INNER_SU_COMMAND as a single-quoted string to su -c
# The single quotes around INNER_SU_COMMAND need to be escaped for the write_file tool.
adb -s "${DROID_IP}:5555" shell su -l "${TERMUX_UID}" -c "${INNER_SU_COMMAND}"