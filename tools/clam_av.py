import os
import platform
import subprocess
import time
import shutil
import logging

# Colors for UI
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Setup logging
logging.basicConfig(filename="data.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

ASCII_ART = r"""

  ____ _        _    __  __    ___     __
 / ___| |      / \  |  \/  |  / \ \   / /
| |   | |     / _ \ | |\/| | / _ \ \ / /
| |___| |___ / ___ \| |  | |/ ___ \ V /
 \____|_____/_/   \_\_|  |_/_/   \_\_/


Welcome to the Ultimate Virus Scanner Toolkit!
"""


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def display_ascii_art():
    """Display the ASCII art title."""
    print(f"{GREEN}{ASCII_ART}{RESET}")


def pause_for_user():
    """Prompt user to press any key to return to the main menu."""
    input(f"{CYAN}Press any key to return to the main menu...{RESET}")
    clear_screen()


def loading_animation(task, process):
    """Dynamic loading animation with real progress."""
    print(f"{CYAN}{task}:{RESET}")
    percentage = 0
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            percentage += 5  # Simulate progress increment (adjust as needed)
            if percentage > 100:
                percentage = 100
            print(f"\r{YELLOW}[{percentage}%]{RESET}", end="", flush=True)
            time.sleep(0.1)
    print(f"\n{GREEN}Done!{RESET}")


def run_with_dynamic_progress(command, task_description):
    """Run a subprocess command with dynamic progress and interface cleanup."""
    try:
        print(f"{CYAN}[INFO] {task_description}...{RESET}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        loading_animation(task_description, process)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"{RED}[ERROR] {stderr.strip()}{RESET}")
            logging.error(f"{task_description} failed: {stderr.strip()}")
        else:
            print(f"{GREEN}[SUCCESS] {task_description} completed successfully!{RESET}")
        time.sleep(2)
    except FileNotFoundError:
        print(f"{RED}[ERROR] Command not found: {command[0]}{RESET}")
        logging.error(f"Command not found: {command[0]}")
    except Exception as e:
        print(f"{RED}[ERROR] {str(e)}{RESET}")
        logging.error(f"{str(e)}")


def detect_environment_and_install():
    """Detect the environment and install ClamAV if not already installed."""
    clear_screen()
    print(f"{CYAN}[INFO] Detecting environment...{RESET}")
    system = platform.system().lower()
    pkg_manager = None
    environment = "Unknown"

    if system == "linux":
        if os.path.exists("/data/data/com.termux/files/usr/bin/bash"):
            pkg_manager = "pkg"
            environment = "Termux on Android"
        elif shutil.which("apt-get"):
            pkg_manager = "apt-get"
            environment = "Debian/Ubuntu-based Linux"
        elif shutil.which("dnf"):
            pkg_manager = "dnf"
            environment = "Fedora-based Linux"
        elif shutil.which("yum"):
            pkg_manager = "yum"
            environment = "RHEL/CentOS-based Linux"
    elif system == "darwin" and shutil.which("brew"):
        pkg_manager = "brew"
        environment = "macOS"
    elif system == "windows":
        print(f"{RED}[ERROR] Windows is not supported for this script.{RESET}")
        logging.error("Unsupported operating system: Windows")
        exit(1)

    print(f"{CYAN}[INFO] Detected environment: {environment}{RESET}")
    print(f"{CYAN}[INFO] Using package manager: {pkg_manager}{RESET}")

    if not shutil.which("clamscan"):
        print(f"{CYAN}[INFO] ClamAV not found. Installing...{RESET}")
        run_with_dynamic_progress([pkg_manager, "install", "-y", "clamav"], "Installing ClamAV")
    else:
        print(f"{GREEN}[INFO] ClamAV is already installed.{RESET}")
        time.sleep(2)
        clear_screen()


def list_files_and_directories():
    """List files and directories for user selection, including root directories on mobile."""
    root_dirs = ["/storage/emulated/0", "/sdcard", "/"]
    for root_dir in root_dirs:
        if os.path.exists(root_dir):
            print(f"{CYAN}Root Folder: {root_dir}{RESET}")
            items = os.listdir(root_dir)
            for i, item in enumerate(items, 1):
                print(f"{GREEN}{i}.{RESET} {item}")
            print()

            choice = input(f"{WHITE}Enter the number of the item to scan (or 0 to cancel): {RESET}")
            if choice.isdigit() and 0 < int(choice) <= len(items):
                return os.path.join(root_dir, items[int(choice) - 1])
    print(f"{RED}[ERROR] No valid selection!{RESET}")
    return None


def scan_files():
    """Scan files or directories for viruses."""
    selected_path = list_files_and_directories()
    if not selected_path:
        return

    options = input(f"{WHITE}Enter additional ClamAV options (or press Enter to use default): {RESET}")
    command = ["clamscan", "-r", selected_path]
    if options:
        command.extend(options.split())

    print(f"{CYAN}[INFO] Starting virus scan on {selected_path}...{RESET}")
    run_with_dynamic_progress(command, "Scanning Files/Directories")
    pause_for_user()


def quarantine_infected_files():
    """Move infected files to a quarantine directory."""
    quarantine_dir = "./quarantine"
    os.makedirs(quarantine_dir, exist_ok=True)
    print(f"{CYAN}[INFO] Moving infected files to {quarantine_dir}...{RESET}")
    run_with_dynamic_progress(["clamscan", "--move", quarantine_dir, "-r", "."], "Quarantining Infected Files")
    pause_for_user()


def update_database():
    """Update the ClamAV virus database."""
    print(f"{CYAN}[INFO] Updating virus database...{RESET}")
    run_with_dynamic_progress(["freshclam"], "Updating Virus Database")
    pause_for_user()


def reset_logs():
    """Reset the error log."""
    with open("data.log", "w") as log_file:
        log_file.truncate()
    print(f"{GREEN}[INFO] Logs cleared successfully.{RESET}")
    pause_for_user()


def show_menu():
    """Display the main menu."""
    display_ascii_art()
    print(f"""{CYAN}
┌───────────────────────────────────────────────┐
│                VIRUS SCANNER TOOLKIT          │
├───────────────────────────────────────────────┤
│ {GREEN}1. Scan Files or Directories{CYAN}                    │
│ {GREEN}2. Update Virus Database{CYAN}                        │
│ {GREEN}3. Quarantine Infected Files{CYAN}                    │
│ {GREEN}4. View Logs (data.log){CYAN}                          │
│ {GREEN}5. Reset Logs{CYAN}                                   │
│ {GREEN}6. Exit{CYAN}                                         │
└───────────────────────────────────────────────┘
{RESET}""")


def main():
    """Main function to run the program."""
    detect_environment_and_install()
    while True:
        show_menu()
        choice = input(f"{WHITE}Choose an option: {RESET}")
        if choice == "1":
            scan_files()
        elif choice == "2":
            update_database()
        elif choice == "3":
            quarantine_infected_files()
        elif choice == "4":
            os.system("cat data.log" if os.name == "posix" else "type data.log")
            pause_for_user()
        elif choice == "5":
            reset_logs()
        elif choice == "6":
            print(f"{GREEN}[INFO] Exiting...{RESET}")
            break
        else:
            print(f"{RED}[ERROR] Invalid option!{RESET}")


if __name__ == "__main__":
    main()
