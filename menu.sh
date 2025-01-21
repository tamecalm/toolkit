#!/bin/bash

# Log and error files
LOG_FILE="logs.csv"
ERROR_LOG="err.txt"

# Define theme colors
DARK_GREEN="\e[1;32m"
DARK_CYAN="\e[1;36m"
DARK_RED="\e[1;31m"
DARK_BOLD="\e[1m"
DARK_RESET="\e[0m"


# Theme and owner details
OWNER_NAME="John"
GITHUB_REPO="https://github.com/tamecalm/toolkit"

# Function to log and print messages
log_and_print() {
    local message=$1
    local level=${2:-"INFO"}
    echo "$(date '+%Y-%m-%d %H:%M:%S'), $level, $message" >> "$LOG_FILE"
    echo -e "${DARK_CYAN}[${level}]${DARK_RESET} $message"
}

detect_environment_and_install() {
    log_and_print "Detecting environment and installing necessary tools..."

    # Detect the operating system
    local os=$(uname | tr '[:upper:]' '[:lower:]')

    # Function to check if a package is installed
    is_installed() {
        command -v "$1" &> /dev/null
    }

    if [[ $os == "linux" ]]; then
        if [[ -d "$PREFIX" && -n "$(echo $PREFIX | grep 'com.termux')" ]]; then
            log_and_print "Termux environment detected. Checking dependencies..."
            required_packages=("python" "curl" "jq" "git")
            for pkg in "${required_packages[@]}"; do
                if is_installed "$pkg"; then
                    log_and_print "$pkg is already installed."
                else
                    log_and_print "Installing $pkg..."
                    pkg install -y "$pkg"
                fi
            done
        else
            log_and_print "Linux environment detected. Checking distribution..."

            # First, try using lsb_release
            local distro
            if command -v lsb_release &> /dev/null; then
                distro=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
                log_and_print "Detected distribution using lsb_release: $distro"
            else
                log_and_print "lsb_release not found. Trying alternative methods..."
                # Try reading /etc/os-release
                if [[ -f /etc/os-release ]]; then
                    distro=$(grep '^ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')
                    log_and_print "Detected distribution using /etc/os-release: $distro"
                else
                    # If both methods fail, fallback to 'unknown'
                    distro="unknown"
                    log_and_print "Unable to detect distribution. Using fallback 'unknown'."
                fi
            fi

            case $distro in
                "ubuntu"|"debian")
                    log_and_print "Ubuntu/Debian detected. Installing dependencies..."
                    sudo apt update
                    for pkg in "python3" "curl" "jq" "git"; do
                        if is_installed "$pkg"; then
                            log_and_print "$pkg is already installed."
                        else
                            sudo apt install -y "$pkg"
                        fi
                    done
                    ;;
                "arch")
                    log_and_print "Arch Linux detected. Installing dependencies..."
                    sudo pacman -Syu --noconfirm
                    for pkg in "python3" "curl" "jq" "git"; do
                        if is_installed "$pkg"; then
                            log_and_print "$pkg is already installed."
                        else
                            sudo pacman -S --noconfirm "$pkg"
                        fi
                    done
                    ;;
                "fedora"|"redhat")
                    log_and_print "Fedora/RedHat detected. Installing dependencies..."
                    sudo dnf install -y python3 curl jq git
                    ;;
                *)
                    log_and_print "Unsupported Linux distribution or detection failed. Please install dependencies manually." "ERROR"
                    exit 1
                    ;;
            esac
        fi
    elif [[ $os == "darwin" ]]; then
        log_and_print "macOS detected. Ensuring Homebrew and dependencies are installed..."
        if ! command -v brew &> /dev/null; then
            log_and_print "Homebrew not found. Please install Homebrew first." "ERROR"
            exit 1
        fi
        for pkg in "python" "jq" "curl" "git"; do
            if is_installed "$pkg"; then
                log_and_print "$pkg is already installed."
            else
                brew install "$pkg"
            fi
        done
    elif [[ $os == "windows_nt" || $os == "msys" || $os == "mingw"* ]]; then
        log_and_print "Windows or Git Bash detected. Checking for Git Bash environment..."
        if command -v git &> /dev/null && git --version | grep -q "git version"; then
            log_and_print "Git Bash detected. Ensure dependencies are installed via pacman or manual setup."
            required_packages=("python" "curl" "jq" "git")
            for pkg in "${required_packages[@]}"; do
                if is_installed "$pkg"; then
                    log_and_print "$pkg is already installed."
                else
                    log_and_print "Installing $pkg using pacman..."
                    pacman -S --noconfirm "$pkg" || log_and_print "Failed to install $pkg. Install it manually." "ERROR"
                fi
            done
        else
            log_and_print "Windows detected. Ensure dependencies (Python, curl, jq, git) are installed manually." "INFO"
        fi
    else
        log_and_print "Unsupported operating system. Please set up dependencies manually." "ERROR"
        exit 1
    fi

    log_and_print "Environment setup and tool verification complete."
}

# Main menu
main_menu() {
    while true; do
        clear

        term_width=$(tput cols)
        x=$(( (term_width - 40) / 2 ))

        # Banner without color and centered
        banner="
   ██╗ ██████╗ ██╗  ██╗███╗   ██╗
   ██║██╔═══██╗██║  ██║████╗  ██║
   ██║██║   ██║███████║██╔██╗ ██║
   ██║██║   ██║██╔══██║██║╚██╗██║
   ██║╚██████╔╝██║  ██║██║ ╚████║
   ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
"

        # Get the terminal width
        cols=$(tput cols)

        # Calculate the length of the banner (longest line)
        banner_length=$(echo "$banner" | wc -L)

        # Calculate padding to center the banner
        padding=$(( (cols - banner_length) / 2 ))

        # Print the banner centered
        while IFS= read -r line; do
            printf "%*s%s\n" $padding "" "$line"
        done <<< "$banner"

        echo -e "${DARK_CYAN}${DARK_BOLD}"
        printf "%*s===========================================\n" $x ""
        echo -e "${DARK_RESET}"

        while true; do
            # Main menu
            echo "Choose an option:"
            echo -e "\n${DARK_GREEN}" \
                "\t1. Network Tools\n" \
                "\t2. System Tools\n" \
                "\t3. Miscellaneous\n" \
                "\t0. Exit"

            echo -e "\n${DARK_RESET}Enter your choice: "
            read -r choice

            case $choice in
                1) # Network Tools Sub-menu
                    while true; do
                        echo -e "\n${DARK_GREEN}" \
                            "\t1. Network Speed Test\n" \
                            "\t2. Port Scanner\n" \
                            "\t3. Wi-Fi Analyzer\n" \
                            "\t4. Ping Utility\n" \
                            "\t5. Traceroute\n" \
                            "\t6. Port Forwarding\n" \
                            "\t7. Activate NextDNS\n" \
                            "\t0. Back to Main Menu"

                        echo -e "\n${DARK_RESET}Enter your choice: "
                        read -r choice_network_tools

                        case $choice_network_tools in
                            1) run_script "network_speed_test.py" ;;
                            2) run_script "port_scanner.py" ;;
                            3) run_script "wifi_analyzer.py" ;;
                            4) run_script "ping.py" ;;
                            5) run_script "traceroute.py" ;;
                            6) run_script "port.py" ;;
                            7) run_script "nextdns.py" ;;
                            0) break ;;
                            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
                        esac
                    done
                    ;;
                2) # System Tools Sub-menu
                    while true; do
                        echo -e "\n${DARK_GREEN}" \
                            "\t1. System Info\n" \
                            "\t2. Logs Viewer\n" \
                            "\t3. Virus Scanner\n" \
                            "\t0. Back to Main Menu"

                        echo -e "\n${DARK_RESET}Enter your choice: "
                        read -r choice_system_tools

                        case $choice_system_tools in
                            1) run_script "system_info.py" ;;
                            2) run_script "logs_viewer.py" ;;
                            3) run_script "clam_av.py" ;;
                            0) break ;;
                            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
                        esac
                    done
                    ;;
                3) # Miscellaneous Sub-menu
                    while true; do
                        echo -e "\n${DARK_GREEN}" \
                            "\t1. HTTP Request\n" \
                            "\t2. Install Required Modules\n" \
                            "\t3. Auto Update Script\n" \
                            "\t0. Back to Main Menu"

                        echo -e "\n${DARK_RESET}Enter your choice: "
                        read -r choice_miscellaneous

                        case $choice_miscellaneous in
                            1) run_script "http_request.py" ;;
                            2) run_modules "gen.py" ;;
                            3) auto_update ;;
                            0) break ;;
                            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
                        esac
                    done
                    ;;
                0)
                    clear
                    echo -e "${DARK_GREEN}Exiting...${DARK_RESET}"
                    break
                    ;;
                *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
            esac

            echo -e "${DARK_CYAN}Press any key to return to the main menu...${DARK_RESET}"
            read -r -n 1
        done
    done
}

# Run the detect environment, loading screen, and main menu
detect_environment_and_install
loading_screen
main_menu
