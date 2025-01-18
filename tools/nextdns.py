import os
import sys
import subprocess
import time

# ANSI escape sequences for colored output
RESET = "\033[0m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"

# Function to check if NextDNS CLI is installed
def check_nextdns_installed():
    try:
        subprocess.run(["nextdns", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"{GREEN}[INFO] NextDNS CLI is already installed.{RESET}")
        return True
    except FileNotFoundError:
        print(f"{RED}[ERROR] NextDNS CLI is not installed.{RESET}")
        return False

# Function to install NextDNS CLI
def install_nextdns():
    print(f"{CYAN}[INFO] Installing NextDNS CLI...{RESET}")
    try:
        subprocess.run(
            ["sh", "-c", "$(curl -sL https://nextdns.io/install)"],
            check=True,
        )
        print(f"{GREEN}[SUCCESS] NextDNS CLI installed successfully.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR] Installation failed: {e}{RESET}")

# Function to activate NextDNS
def activate_nextdns(profile_id):
    print(f"{CYAN}[INFO] Activating NextDNS with Profile ID: {profile_id}...{RESET}")
    try:
        subprocess.run(["nextdns", "activate", f"--profile={profile_id}"], check=True)
        print(f"{GREEN}[SUCCESS] NextDNS is now active.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR] Activation failed: {e}{RESET}")

# Function to deactivate NextDNS
def deactivate_nextdns():
    print(f"{CYAN}[INFO] Deactivating NextDNS...{RESET}")
    try:
        subprocess.run(["nextdns", "deactivate"], check=True)
        print(f"{GREEN}[SUCCESS] NextDNS is now deactivated.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR] Deactivation failed: {e}{RESET}")

# Function to view NextDNS logs
def view_nextdns_logs():
    print(f"{CYAN}[INFO] Displaying NextDNS logs...{RESET}")
    try:
        subprocess.run(["nextdns", "log"])
    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR] Unable to display logs: {e}{RESET}")

# Menu to manage NextDNS CLI
def main_menu():
    while True:
        os.system("clear")
        print(f"{GREEN}--- NextDNS Manager ---{RESET}".center(50))
        print(f"{CYAN}Use this tool to install, configure, and manage NextDNS CLI.{RESET}".center(50))
        print(f"\n{GREEN}Main Menu:{RESET}")
        print(f"{CYAN}1. Install NextDNS CLI{RESET}")
        print(f"{CYAN}2. Activate NextDNS{RESET}")
        print(f"{CYAN}3. Deactivate NextDNS{RESET}")
        print(f"{CYAN}4. View NextDNS Logs{RESET}")
        print(f"{CYAN}5. Exit{RESET}")
        
        choice = input(f"\n{GREEN}Select an option: {RESET}")
        
        if choice == "1":
            install_nextdns()
        elif choice == "2":
            profile_id = input(f"{CYAN}Enter NextDNS Profile ID: {RESET}")
            activate_nextdns(profile_id)
        elif choice == "3":
            deactivate_nextdns()
        elif choice == "4":
            view_nextdns_logs()
        elif choice == "5":
            print(f"{GREEN}Exiting...{RESET}")
            break
        else:
            print(f"{RED}[ERROR] Invalid choice. Please try again.{RESET}")
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

# Entry point
if __name__ == "__main__":
    main_menu()