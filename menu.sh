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

# Function to display an animated loading screen
loading_screen() {
    clear

    frames=(
        "  ██████   ██████   ██████   ██████   ██████   ██████   ██████  "
        " ████████ ████████ ████████ ████████ ████████ ████████ ████████ "
        "██████████████████████████████████████████████████████████████"
        "██████████████████████████████████████████████████████████████"
        " ████████ ████████ ████████ ████████ ████████ ████████ ████████ "
        "  ██████   ██████   ██████   ██████   ██████   ██████   ██████  "
    )

    echo -e "${DARK_CYAN}${DARK_BOLD}"
    for frame in "${frames[@]}"; do
        echo -e "\n\n\n\n\n\n\n\t\t$frame"
        sleep 0.2
        clear
    done

    for i in {1..100}; do
        printf "\r\t\tLoading... %d%%" "$i"
        sleep 0.02
    done

    echo -e "\n\n\t${DARK_GREEN}[INFO] Toolkit Loaded Successfully!${DARK_RESET}"
    sleep 1
}

# Function to auto-update the script from GitHub using curl
auto_update() {
    echo -e "${DARK_CYAN}[INFO] Checking for updates...${DARK_RESET}"

    # Directory where the script is located
    SCRIPT_DIR="$(dirname "$(realpath "$0")")"

    # GitHub URL for the repository
    BASE_URL="https://raw.githubusercontent.com/tamecalm/toolkit/main"

    # Update menu.sh
    echo -e "${DARK_CYAN}[INFO] Updating menu.sh...${DARK_RESET}"
    curl -s "$BASE_URL/menu.sh" -o "$SCRIPT_DIR/menu.sh"
    chmod +x "$SCRIPT_DIR/menu.sh"

    # Update all Python scripts in the tools folder
    echo -e "${DARK_CYAN}[INFO] Updating Python scripts in the tools folder...${DARK_RESET}"
    for script in $(ls "$SCRIPT_DIR/tools"/*.py); do
        script_name=$(basename "$script")
        curl -s "$BASE_URL/tools/$script_name" -o "$SCRIPT_DIR/tools/$script_name"
    done

    # Update all Python scripts outside the tools folder
    echo -e "${DARK_CYAN}[INFO] Updating Python scripts outside the tools folder...${DARK_RESET}"
    for script in $(ls "$SCRIPT_DIR"/*.py); do
        script_name=$(basename "$script")
        curl -s "$BASE_URL/$script_name" -o "$SCRIPT_DIR/$script_name"
    done

    # Update README.md
    echo -e "${DARK_CYAN}[INFO] Updating README.md...${DARK_RESET}"
    curl -s "$BASE_URL/README.md" -o "$SCRIPT_DIR/README.md"

    # Update requirements.txt
    echo -e "${DARK_CYAN}[INFO] Updating requirements.txt...${DARK_RESET}"
    curl -s "$BASE_URL/requirements.txt" -o "$SCRIPT_DIR/requirements.txt"

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

        echo -e "${DARK_CYAN}${DARK_BOLD}"
        echo "  ==========================================="
        echo "           Welcome to $OWNER_NAME's Toolkit            "
        echo "  ==========================================="
        echo -e "${DARK_RESET}"

        echo "Choose an option:"
        echo -e "\n${DARK_GREEN}" \
             "\t1. Encrypt a File\n" \
             "\t2. Decrypt a File\n" \
             "\t3. Network Speed Test\n" \
             "\t4. System Health Check\n" \
             "\t5. Schedule a Task\n" \
             "\t6. Port Scanner\n" \
             "\t7. Wi-Fi Analyzer\n" \
             "\t8. Bluetooth Scanner\n" \
             "\t9. Media Downloader\n" \
             "\t10. Auto Update Script\n" \
             "\t0. Exit"

        echo -e "\n${DARK_RESET}Enter your choice: "
        read -r choice

        case $choice in
            1) run_script "encrypt_file.py" ;;
            2) run_script "decrypt_file.py" ;;
            3) run_script "network_speed_test.py" ;;
            4) run_script "system_health.py" ;;
            5) run_script "schedule_task.py" ;;
            6) run_script "port_scanner.py" ;;
            7) run_script "wifi_analyzer.py" ;;
            8) run_script "bluetooth_scanner.py" ;;
            9) run_script "media_downloader.py" ;;
            10) auto_update ;;
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
