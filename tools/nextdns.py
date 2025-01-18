import os
import sys
import subprocess

# ANSI escape sequences for colored output
RESET = "\033[0m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"

# Function to detect the operating system
def detect_environment():
    os_name = sys.platform
    if "linux" in os_name and "android" in os.uname().release.lower():
        return "termux"
    elif os_name == "linux":
        return "linux"
    elif os_name == "darwin":
        return "macos"
    elif os_name.startswith("win"):
        return "windows"
    else:
        return "unsupported"

# Function to configure DNS-over-TLS for Termux (Android)
def configure_termux_dot():
    print(f"{CYAN}[INFO] Configuring DNS-over-TLS (DoT) for Termux...{RESET}")
    resolv_conf_path = os.path.join(os.getenv("PREFIX"), "etc", "resolv.conf")
    try:
        with open(resolv_conf_path, "w") as resolv_file:
            resolv_file.write("nameserver 45.90.28.0\n")
            resolv_file.write("nameserver 45.90.30.0\n")
        print(f"{GREEN}[SUCCESS] DNS-over-TLS configured for Termux.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Failed to configure DoT: {e}{RESET}")

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
    environment = detect_environment()

    if environment == "unsupported":
        print(f"{RED}[ERROR] Unsupported operating system.{RESET}")
        return

    while True:
        os.system("clear")
        print(f"{GREEN}--- NextDNS Manager ({environment.upper()}) ---{RESET}".center(50))
        print(f"{CYAN}Use this tool to install, configure, and manage NextDNS CLI.{RESET}".center(50))
        print(f"\n{GREEN}Main Menu:{RESET}")
        print(f"{CYAN}1. Install NextDNS CLI{RESET}")
        print(f"{CYAN}2. Activate NextDNS{RESET}")
        print(f"{CYAN}3. Deactivate NextDNS{RESET}")
        print(f"{CYAN}4. View NextDNS Logs{RESET}")
        print(f"{CYAN}5. Configure DNS-over-TLS (DoT) [Termux Only]{RESET}")
        print(f"{CYAN}6. Exit{RESET}")
        
        choice = input(f"\n{GREEN}Select an option: {RESET}")
        
        if choice == "1":
            if environment in ["linux", "macos"]:
                install_nextdns()
            else:
                print(f"{RED}[ERROR] Installation is not supported in this environment.{RESET}")
        elif choice == "2":
            profile_id = input(f"{CYAN}Enter NextDNS Profile ID: {RESET}")
            if environment in ["linux", "macos"]:
                activate_nextdns(profile_id)
            else:
                print(f"{RED}[ERROR] Activation is not supported in this environment.{RESET}")
        elif choice == "3":
            if environment in ["linux", "macos"]:
                deactivate_nextdns()
            else:
                print(f"{RED}[ERROR] Deactivation is not supported in this environment.{RESET}")
        elif choice == "4":
            if environment in ["linux", "macos"]:
                view_nextdns_logs()
            else:
                print(f"{RED}[ERROR] Logs are not supported in this environment.{RESET}")
        elif choice == "5":
            if environment == "termux":
                configure_termux_dot()
            else:
                print(f"{RED}[ERROR] DoT configuration is only for Termux (Android).{RESET}")
        elif choice == "6":
            print(f"{GREEN}Exiting...{RESET}")
            break
        else:
            print(f"{RED}[ERROR] Invalid choice. Please try again.{RESET}")
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

# Entry point
if __name__ == "__main__":
    main_menu()