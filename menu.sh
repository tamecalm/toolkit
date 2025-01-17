#!/bin/bash

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

# Function to display animated header
animated_header() {
    clear
    term_width=$(tput cols)
    term_height=$(tput lines)

    # Animated hacking-style 3D header
    for i in {1..3}; do
        clear
        for ((line = 1; line <= term_height / 3; line++)); do
            echo
        done
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_GREEN}███████╗████████╗██╗     ██████╗███╗   ██╗"
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_GREEN}██╔════╝╚══██╔══╝██║    ██╔════╝████╗  ██║"
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_GREEN}█████╗     ██║   ██║    ██║     ██╔██╗ ██║"
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_GREEN}██╔══╝     ██║   ██║    ██║     ██║╚██╗██║"
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_GREEN}███████╗   ██║   ██║    ╚██████╗██║ ╚████║"
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_GREEN}╚══════╝   ╚═╝   ╚═╝     ╚═════╝╚═╝  ╚═══╝"
        printf "%*s%s\n" $(( (term_width - 36) / 2 )) "" "${DARK_BOLD}${DARK_CYAN}Welcome to ${OWNER_NAME}'s Toolkit"
        sleep 0.2
    done
    echo -e "${DARK_RESET}"
}

# Function to auto-update the script from GitHub
auto_update() {
    echo -e "${DARK_CYAN}[INFO] Checking for updates...${DARK_RESET}"

    SCRIPT_DIR="$(dirname "$(realpath "$0")")"
    API_URL="https://api.github.com/repos/tamecalm/toolkit/contents"

    update_files() {
        local api_url="$1"
        local dest_dir="$2"
        json_data=$(curl -s "$api_url")

        if [[ -z "$json_data" ]]; then
            echo -e "${DARK_RED}[ERROR] Failed to fetch repository data.${DARK_RESET}"
            return
        fi

        echo "$json_data" | jq -c '.[]' | while read -r item; do
            item_type=$(echo "$item" | jq -r '.type')
            item_path=$(echo "$item" | jq -r '.path')
            download_url=$(echo "$item" | jq -r '.download_url')
            dest_file="$dest_dir/$item_path"

            if [[ $item_type == "dir" ]]; then
                mkdir -p "$dest_file"
                update_files "$API_URL/$item_path" "$dest_dir"
            elif [[ $item_type == "file" ]]; then
                echo -e "${DARK_CYAN}[INFO] Updating $item_path...${DARK_RESET}"
                curl -s "$download_url" -o "$dest_file"
            fi
        done
    }

    update_files "$API_URL" "$SCRIPT_DIR"
    find "$SCRIPT_DIR" -name "*.sh" -exec chmod +x {} \;
    echo -e "${DARK_GREEN}[INFO] Update completed. Restarting...${DARK_RESET}"
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
        animated_header
        echo -e "${DARK_GREEN}Main Menu:${DARK_RESET}"
        echo -e "\n1. Network Tools"
        echo -e "2. System Tools"
        echo -e "3. Script Manager"
        echo -e "0. Exit"

        echo -e "\nEnter your choice: "
        read -r main_choice

        case $main_choice in
            1) network_tools_menu ;;
            2) system_tools_menu ;;
            3) auto_update ;;
            0) echo -e "${DARK_GREEN}Goodbye!${DARK_RESET}"; exit ;;
            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
        esac

        echo -e "${DARK_CYAN}Press any key to return to the main menu...${DARK_RESET}"
        read -r -n 1
    done
}

# Submenu for Network Tools
network_tools_menu() {
    while true; do
        clear
        animated_header
        echo -e "${DARK_CYAN}Network Tools:${DARK_RESET}"
        echo -e "\n1. Network Speed Test"
        echo -e "2. Port Scanner"
        echo -e "3. Wi-Fi Analyzer"
        echo -e "0. Back to Main Menu"

        echo -e "\nEnter your choice: "
        read -r choice

        case $choice in
            1) run_script "network_speed_test.py" ;;
            2) run_script "port_scanner.py" ;;
            3) run_script "wifi_analyzer.py" ;;
            0) return ;;
            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
        esac
    done
}

# Submenu for System Tools
system_tools_menu() {
    while true; do
        clear
        animated_header
        echo -e "${DARK_CYAN}System Tools:${DARK_RESET}"
        echo -e "\n1. System Info"
        echo -e "2. Ping Utility"
        echo -e "3. Traceroute"
        echo -e "0. Back to Main Menu"

        echo -e "\nEnter your choice: "
        read -r choice

        case $choice in
            1) run_script "system_info.py" ;;
            2) run_script "ping.py" ;;
            3) run_script "traceroute.py" ;;
            0) return ;;
            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
        esac
    done
}

# Run the main menu
main_menu