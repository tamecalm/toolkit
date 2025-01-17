#!/bin/bash

# Ensure the script runs with wake lock enabled if on Termux
if [[ $(uname -o) == "Android" ]]; then
    termux-wake-lock
fi

# Log and error files
LOG_FILE="logs.csv"
ERROR_LOG="err.txt"

# Define theme colors
DARK_GREEN="\033[1;32m"
DARK_CYAN="\033[1;36m"
DARK_RED="\033[1;31m"
DARK_BOLD="\033[1m"
DARK_RESET="\033[0m"

# Theme and owner details
OWNER_NAME="John"
GITHUB_REPO="https://github.com/tamecalm/toolkit"
FOOTER="\033[3m""'Stay Calm, Stay Focused' - @tamecalm\033[0m"

# Function to display an animated loading screen
loading_screen() {
    clear

    frames=(
        "        ██████   ██████   ██████   ██████   ██████   ██████   ██████        "
        "       ████████ ████████ ████████ ████████ ████████ ████████ ████████       "
        "      ███████████████████████████████████████████████████████████████      "
        "       ████████ ████████ ████████ ████████ ████████ ████████ ████████       "
        "        ██████   ██████   ██████   ██████   ██████   ██████   ██████        "
    )

    term_width=$(tput cols)
    term_height=$(tput lines)

    for frame in "${frames[@]}"; do
        clear
        frame_width=${#frame}
        x=$(( (term_width - frame_width) / 2 ))
        y=$(( (term_height - 7) / 2 ))

        for ((i = 0; i < y; i++)); do
            echo
        done

        printf "%*s%s\n" $x "" "$frame"
        sleep 0.2
    done

    for i in {1..100}; do
        clear
        loading_text="Loading... $i%%"
        loading_width=${#loading_text}
        x=$(( (term_width - loading_width) / 2 ))
        y=$(( (term_height - 1) / 2 ))

        for ((j = 0; j < y; j++)); do
            echo
        done

        printf "%*s%s\n" $x "" "$loading_text"
        sleep 0.02
    done
}

# Function to auto-update the script from GitHub using curl
auto_update() {
    echo -e "${DARK_CYAN}[INFO] Checking for updates...${DARK_RESET}"

    # Directory where the script is located
    SCRIPT_DIR="$(dirname "$(realpath "$0")")"

    # GitHub URL for the repository
    BASE_URL="https://raw.githubusercontent.com/tamecalm/toolkit/main"

    # Fetch file listing from GitHub repo
    echo -e "${DARK_CYAN}[INFO] Fetching file listing from the repository...${DARK_RESET}"
    repo_files=$(curl -s "https://api.github.com/repos/tamecalm/toolkit/contents" | grep '"path"' | cut -d '"' -f 4)

    if [[ -z "$repo_files" ]]; then
        echo -e "${DARK_RED}[ERROR] Failed to fetch file listing. Ensure you have internet access and the repository URL is correct.${DARK_RESET}"
        return
    fi

    # Loop through all files in the repository and update or download new ones
    for file in $repo_files; do
        dest_file="$SCRIPT_DIR/$file"

        # Create directories for nested files if they don't exist
        dest_dir=$(dirname "$dest_file")
        mkdir -p "$dest_dir"

        # Download file from GitHub
        echo -e "${DARK_CYAN}[INFO] Updating $file...${DARK_RESET}"
        curl -s "$BASE_URL/$file" -o "$dest_file"
    done

    # Make all .sh files executable
    find "$SCRIPT_DIR" -name "*.sh" -exec chmod +x {} \;

    echo -e "${DARK_GREEN}[INFO] Update completed. Restarting...${DARK_RESET}"

    # Restart the updated menu.sh
    exec "$SCRIPT_DIR/menu.sh"
}

# Function to handle errors
handle_error() {
    local error_message=$1
    echo -e "${DARK_RED}[ERROR] ${error_message}${DARK_RESET}"
    echo "$(date '+%Y-%m-%d %H:%M:%S'), $error_message" >> "$ERROR_LOG"
}

# Function to execute a Python script
run_script() {
    local script_name=$1
    python3 "tools/$script_name" || handle_error "Failed to run $script_name"
}

# Main menu
main_menu() {
    while true; do
        clear

        term_width=$(tput cols)
        x=$(( (term_width - 40) / 2 ))

        echo -e "${DARK_CYAN}${DARK_BOLD}"
        printf "%*s===========================================\n" $x ""
        printf "%*sWelcome to $OWNER_NAME's Toolkit\n" $x ""
        printf "%*s===========================================\n" $x ""
        echo -e "${DARK_RESET}"

        echo "Choose an option:"
        echo -e "\n${DARK_GREEN}" \
             "\t1. Network Speed Test\n" \
             "\t2. Port Scanner\n" \
             "\t3. Wi-Fi Analyzer\n" \
             "\t4. System Info\n" \
             "\t5. Ping Utility\n" \
             "\t6. Traceroute\n" \
             "\t7. Port Forwarding\n" \
             "\t8. Auto Update Script\n" \
             "\t0. Exit"

        echo -e "\n${DARK_RESET}Enter your choice: "
        read -r choice

        case $choice in
            1) run_script "network_speed_test.py" ;;
            2) run_script "port_scanner.py" ;;
            3) run_script "wifi_analyzer.py" ;;
            4) run_script "system_info.py" ;;
            5) run_script "ping.py" ;;
            6) run_script "traceroute.py" ;;
            7) run_script "port.py" ;;
            8) auto_update ;;
            0) echo -e "${DARK_GREEN}Exiting...${DARK_RESET}"; break ;;
            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
        esac

        echo -e "${DARK_CYAN}Press any key to return to the main menu...${DARK_RESET}"
        read -r -n 1
    done
}

# Run the loading screen and main menu
loading_screen
main_menu

# Display footer at exit
clear
echo -e "$FOOTER"