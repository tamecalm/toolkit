import os
import platform
import subprocess
import shutil
import logging
import sys
from shutil import which

# Color codes for hacking-themed UI
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Logging setup
logging.basicConfig(
    filename="data.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ASCII_ART = r"""
  ███╗   ██╗ █████╗ ██████╗ ██╗  ██╗██╗███╗   ███╗
  ████╗  ██║██╔══██╗██╔══██╗██║ ██╔╝██║████╗ ████║
  ██╔██╗ ██║███████║██████╔╝█████╔╝ ██║██╔████╔██║
  ██║╚██╗██║██╔══██║██╔═══╝ ██╔═██╗ ██║██║╚██╔╝██║
  ██║ ╚████║██║  ██║██║     ██║  ██╗██║██║ ╚═╝ ██║
  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝

       LOG VIEWER AND ANALYSIS TOOLKIT
       For Cyber Enthusiasts and Analysts
"""

def log_and_print(message, level="INFO"):
    """Log a message and print it to the console."""
    levels = {"INFO": logging.info, "ERROR": logging.error, "WARNING": logging.warning}
    print(f"{CYAN}[{level}] {message}{RESET}")
    levels[level](message)


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def display_banner():
    """Display the banner art."""
    print(f"{GREEN}{ASCII_ART}{RESET}")


def pause_for_user():
    """Prompt user to press any key to return to the main menu."""
    input(f"{CYAN}Press any key to return to the main menu...{RESET}")
    clear_screen()


def detect_environment_and_install():
    """Detect the environment and install necessary tools."""
    try:
        log_and_print("Detecting environment...", level="INFO")

        # Detect platform
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO")

        if system == "linux":
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Termux environment detected. Installing required tools...", level="INFO")
                subprocess.run(["pkg", "install", "-y", "python", "coreutils"], check=True)
            else:
                distro = platform.linux_distribution()[0].lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing required tools...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "python3", "coreutils"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing required tools...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "python", "coreutils"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing required tools...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "python3", "coreutils"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install the required tools manually.", level="ERROR")
                    sys.exit(1)

        elif system == "darwin":
            log_and_print("macOS detected. Installing required tools via Homebrew...", level="INFO")
            subprocess.run(["brew", "install", "python"], check=True)

        elif system == "windows":
            log_and_print("Windows detected. Checking for required tools...", level="INFO")
            if not which("python"):
                log_and_print("Python not found. Please install it manually.", level="ERROR")
                sys.exit(1)

        else:
            log_and_print("Unsupported system. Please install the required tools manually.", level="ERROR")
            sys.exit(1)

    except Exception as e:
        log_and_print(f"Error during environment detection: {str(e)}", level="ERROR")
        sys.exit(1)


def view_logs():
    """Display the logs with an option to filter."""
    clear_screen()
    display_banner()
    print(f"{CYAN}Viewing logs...{RESET}")
    if not os.path.exists("data.log"):
        log_and_print("Log file does not exist!", level="ERROR")
        pause_for_user()
        return

    print(f"{CYAN}Do you want to filter logs? (y/n): {RESET}", end="")
    choice = input().strip().lower()
    if choice == "y":
        keyword = input(f"{WHITE}Enter a keyword to filter logs: {RESET}")
        print(f"{CYAN}\nFiltered Logs:{RESET}")
        with open("data.log", "r") as log_file:
            for line in log_file:
                if keyword.lower() in line.lower():
                    print(f"{GREEN}{line.strip()}{RESET}")
    else:
        print(f"{CYAN}\nFull Logs:{RESET}")
        with open("data.log", "r") as log_file:
            print(log_file.read())

    pause_for_user()


def analyze_logs():
    """Analyze logs for patterns or anomalies."""
    clear_screen()
    display_banner()
    print(f"{CYAN}Analyzing logs...{RESET}")
    if not os.path.exists("data.log"):
        log_and_print("Log file does not exist!", level="ERROR")
        pause_for_user()
        return

    errors = []
    warnings = []
    with open("data.log", "r") as log_file:
        for line in log_file:
            if "ERROR" in line:
                errors.append(line.strip())
            elif "WARNING" in line:
                warnings.append(line.strip())

    print(f"{CYAN}Log Analysis Report:{RESET}")
    print(f"{RED}Errors ({len(errors)}):{RESET}")
    for error in errors:
        print(f"{RED}- {error}{RESET}")
    print(f"{YELLOW}\nWarnings ({len(warnings)}):{RESET}")
    for warning in warnings:
        print(f"{YELLOW}- {warning}{RESET}")

    pause_for_user()


def reset_logs():
    """Reset the log file."""
    clear_screen()
    display_banner()
    print(f"{CYAN}Resetting logs...{RESET}")
    with open("data.log", "w") as log_file:
        log_file.truncate()
    log_and_print("Logs have been cleared successfully.", level="INFO")
    pause_for_user()


def user_guide():
    """Display the user guide."""
    clear_screen()
    display_banner()
    print(f"""{CYAN}
USER GUIDE:
1. View Logs:
   - View all logs or filter by specific keywords.

2. Analyze Logs:
   - Summarizes errors and warnings for quick debugging.

3. Reset Logs:
   - Clears all logs to start fresh.

4. Environment Detection:
   - Automatically detects your environment and installs dependencies.

Press any key to return to the main menu...{RESET}""")
    pause_for_user()


def show_menu():
    """Display the main menu."""
    display_banner()
    print(f"""{CYAN}
┌───────────────────────────────────────────────┐
│               LOG ANALYSIS TOOLKIT            │
├───────────────────────────────────────────────┤
│ {GREEN}1. View Logs{CYAN}                                   │
│ {GREEN}2. Analyze Logs{CYAN}                               │
│ {GREEN}3. Reset Logs{CYAN}                                 │
│ {GREEN}4. User Guide{CYAN}                                 │
│ {GREEN}5. Exit{CYAN}                                       │
└───────────────────────────────────────────────┘
{RESET}""")


def main():
    """Main function to run the program."""
    detect_environment_and_install()
    while True:
        show_menu()
        choice = input(f"{WHITE}Choose an option: {RESET}")
        if choice == "1":
            view_logs()
        elif choice == "2":
            analyze_logs()
        elif choice == "3":
            reset_logs()
        elif choice == "4":
            user_guide()
        elif choice == "5":
            log_and_print("Exiting the program...", level="INFO")
            break
        else:
            log_and_print("Invalid option!", level="ERROR")
            pause_for_user()


if __name__ == "__main__":
    main()
