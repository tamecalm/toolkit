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

# Function to log and print messages
log_and_print() {
    local message=$1
    local level=${2:-"INFO"}
    echo "$(date '+%Y-%m-%d %H:%M:%S'), $level, $message" >> "$LOG_FILE"
    echo -e "${DARK_CYAN}[${level}]${DARK_RESET} $message"
}

# Function to detect environment and install dependencies
detect_environment_and_install() {
    log_and_print "Detecting environment and installing necessary tools..."

    # Detect the operating system
    local os=$(uname | tr '[:upper:]' '[:lower:]')

    if [[ $os == "linux" ]]; then
        if [[ -d "$PREFIX" && -n "$(echo $PREFIX | grep 'com.termux')" ]]; then
            log_and_print "Termux environment detected. Checking dependencies..."
            required_packages=("python" "curl" "jq" "git")
            for pkg in "${required_packages[@]}"; do
                if ! command -v "$pkg" &> /dev/null; then
                    log_and_print "Installing $pkg..."
                    pkg install -y "$pkg"
                else
                    log_and_print "$pkg is already installed."
                fi
            done
        else
            log_and_print "Linux environment detected. Checking distribution..."
            local distro=$(lsb_release -is 2>/dev/null || echo "unknown" | tr '[:upper:]' '[:lower:]')
            case $distro in
                "ubuntu"|"debian")
                    log_and_print "Ubuntu/Debian detected. Installing dependencies..."
                    sudo apt update && sudo apt install -y python3 curl jq git
                    ;;
                "arch")
                    log_and_print "Arch Linux detected. Installing dependencies..."
                    sudo pacman -Syu --noconfirm python3 curl jq git
                    ;;
                "fedora"|"redhat")
                    log_and_print "Fedora/RedHat detected. Installing dependencies..."
                    sudo dnf install -y python3 curl jq git
                    ;;
                *)
                    log_and_print "Unsupported Linux distribution. Please install dependencies manually." "ERROR"
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
        brew install python jq curl git
    elif [[ $os == "windows_nt" ]]; then
        log_and_print "Windows detected. Ensure dependencies (Python, curl, jq, git) are installed manually." "INFO"
    else
        log_and_print "Unsupported operating system. Please set up dependencies manually." "ERROR"
        exit 1
    fi

    log_and_print "Environment setup and tool verification complete."
}

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

# Function to auto-update the script from GitHub
auto_update() {
    echo -e "${DARK_CYAN}[INFO] Checking for updates...${DARK_RESET}"

    # Directory where the script is located
    SCRIPT_DIR="$(dirname "$(realpath "$0")")"

    # GitHub API URL for the repository contents
    API_URL="https://api.github.com/repos/tamecalm/toolkit/contents"

    # Temporary file to store the list of repository files
    REPO_FILES=$(mktemp)

    # Recursive function to fetch and update files
    update_files() {
        local api_url="$1"
        local dest_dir="$2"

        # Fetch JSON data for the current directory
        json_data=$(curl -s "$api_url")

        if [[ -z "$json_data" ]]; then
            echo -e "${DARK_RED}[ERROR] Failed to fetch repository data.${DARK_RESET}"
            return
        fi

        # Loop through items in the JSON data
        echo "$json_data" | jq -c '.[]' | while read -r item; do
            item_type=$(echo "$item" | jq -r '.type')
            item_path=$(echo "$item" | jq -r '.path')
            download_url=$(echo "$item" | jq -r '.download_url')

            dest_file="$dest_dir/$item_path"

            # Add the file path to the repository file list
            echo "$dest_file" >> "$REPO_FILES"

            if [[ $item_type == "dir" ]]; then
                # If it's a directory, create it and recurse
                mkdir -p "$dest_file"
                update_files "$API_URL/$item_path" "$dest_dir"
            elif [[ $item_type == "file" ]]; then
                # Download and update the file
                echo -e "${DARK_CYAN}[INFO] Updating $item_path...${DARK_RESET}"
                curl -s "$download_url" -o "$dest_file"
            fi
        done
    }

    # Start updating files from the repository root
    update_files "$API_URL" "$SCRIPT_DIR"

    # Remove any files that are not in the repository
    echo -e "${DARK_CYAN}[INFO] Cleaning up unnecessary files...${DARK_RESET}"
    find "$SCRIPT_DIR" -type f | while read -r local_file; do
        if ! grep -Fxq "$local_file" "$REPO_FILES"; then
            echo -e "${DARK_RED}[INFO] Removing $local_file...${DARK_RESET}"
            rm -f "$local_file"
        fi
    done

    # Cleanup temporary file
    rm -f "$REPO_FILES"

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

# Function to execute a python script that download required modules
run_modules() {
    local script_name=$1
    python3 "$script_name" || handle_error "Failed to run $script_name"
}

# Main menu
main_menu() {
    while true; do
        clear

        term_width=$(tput cols)
        x=$(( (term_width - 40) / 2 ))

        # Art banner for JOHN
        art=$(cat <<EOF
${DARK_GREEN}
   __     ______     __  __     __   __    
  /\ \   /\  __ \   /\ \_\ \   /\ "-.\ \   
 _\_\ \  \ \ \/\ \  \ \  __ \  \ \ \-.  \  
/\_____\  \ \_____\  \ \_\ \_\  \ \_\\"\_\ 
\/_____/   \/_____/   \/_/\/_/   \/_/ \/_/ 
                                           
${DARK_RESET}
EOF
        )
        printf "%*s\n" $(( (term_width + ${#art}) / 2 )) "$art"

        echo -e "${DARK_CYAN}${DARK_BOLD}"
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
             "\t8. Activate NextDNS\n" \
             "\t9. HTTP Request\n" \
             "\t10. Logs Viewer\n" \
             "\t11. Virus Scanner\n" \
             "\t12. Install Required Modules\n" \
             "\t13. Auto Update Script\n" \
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
            8) run_script "nextdns.py" ;;
            9) run_script "http_request.py" ;;
            10) run_script "logs_viewer.py" ;;
            11) run_script "clam_av.py" ;;
            12) run_modules "gen.py" ;;
            13) auto_update ;;
            0) 
    clear
    echo -e "${DARK_GREEN}Exiting...${DARK_RESET}"
    break
    ;;
          #  0) echo -e "${DARK_GREEN}Exiting...${DARK_RESET}"; break ;;
            *) echo -e "${DARK_RED}Invalid option! Please try again.${DARK_RESET}" ;;
        esac

        echo -e "${DARK_CYAN}Press any key to return to the main menu...${DARK_RESET}"
        read -r -n 1
    done
}

# Run the detect environment, loading screen, and main menu
detect_environment_and_install
loading_screen
main_menu
