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

# Function to display a hacking-style animated header
animated_header() {
    frames=("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
            "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
            "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"
            "█████████████████████████████████████████████████")
    
    for i in {1..3}; do
        for frame in "${frames[@]}"; do
            clear
            term_width=$(tput cols)
            x=$(( (term_width - ${#frame}) / 2 ))
            printf "%*s%s\n" $x "" "$frame"
            sleep 0.1
        done
    done

    clear
    echo -e "${DARK_GREEN}${DARK_BOLD}"
    printf "%*sWelcome to $OWNER_NAME's Toolkit\n" $((($(tput cols) - 30) / 2)) ""
    echo -e "${DARK_RESET}"
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

# Submenu for Network Tools
network_tools_menu() {
    while true; do
        clear
        echo -e "${DARK_CYAN}Network Tools:${DARK_RESET}"
        echo "1. Network Speed Test"
        echo "2. Ping Utility"
        echo "3. Traceroute"
        echo "0. Back to Main Menu"
        echo -n "Enter your choice: "
        read -r choice
        case $choice in
            1) run_script "network_speed_test.py" ;;
            2) run_script "ping.py" ;;
            3) run_script "traceroute.py" ;;
            0) break ;;
            *) echo -e "${DARK_RED}Invalid option!${DARK_RESET}" ;;
        esac
        echo -e "${DARK_CYAN}Press any key to return to the submenu...${DARK_RESET}"
        read -r -n 1
    done
}

# Submenu for Port Tools
port_tools_menu() {
    while true; do
        clear
        echo -e "${DARK_CYAN}Port Tools:${DARK_RESET}"
        echo "1. Port Scanner"
        echo "2. Port Forwarding"
        echo "0. Back to Main Menu"
        echo -n "Enter your choice: "
        read -r choice
        case $choice in
            1) run_script "port_scanner.py" ;;
            2) run_script "port.py" ;;
            0) break ;;
            *) echo -e "${DARK_RED}Invalid option!${DARK_RESET}" ;;
        esac
        echo -e "${DARK_CYAN}Press any key to return to the submenu...${DARK_RESET}"
        read -r -n 1
    done
}

# Submenu for Wi-Fi Tools
wifi_tools_menu() {
    while true; do
        clear
        echo -e "${DARK_CYAN}Wi-Fi Tools:${DARK_RESET}"
        echo "1. Wi-Fi Analyzer"
        echo "0. Back to Main Menu"
        echo -n "Enter your choice: "
        read -r choice
        case $choice in
            1) run_script "wifi_analyzer.py" ;;
            0) break ;;
            *) echo -e "${DARK_RED}Invalid option!${DARK_RESET}" ;;
        esac
        echo -e "${DARK_CYAN}Press any key to return to the submenu...${DARK_RESET}"
        read -r -n 1
    done
}

# Main menu
main_menu() {
    while true; do
        clear
        animated_header
        echo -e "${DARK_CYAN}Main Menu:${DARK_RESET}"
        echo "1. Network Tools"
        echo "2. Port Tools"
        echo "3. Wi-Fi Tools"
        echo "4. System Info"
        echo "5. Auto Update Script"
        echo "0. Exit"
        echo -n "Enter your choice: "
        read -r choice
        case $choice in
            1) network_tools_menu ;;
            2) port_tools_menu ;;
            3) wifi_tools_menu ;;
            4) run_script "system_info.py" ;;
            5) auto_update ;;
            0) echo -e "${DARK_GREEN}Exiting...${DARK_RESET}"; break ;;
            *) echo -e "${DARK_RED}Invalid option!${DARK_RESET}" ;;
        esac
        echo -e "${DARK_CYAN}Press any key to return to the main menu...${DARK_RESET}"
        read -r -n 1
    done
}

# Run the main menu
main_menu