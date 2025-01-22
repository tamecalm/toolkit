import os
import sys
import subprocess
import platform
import time

# ANSI escape sequences for colored output
RESET = "\033[0m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"

# Function to log and print messages
def log_and_print(message, level="INFO"):
    color = GREEN if level == "INFO" else RED
    print(f"{color}[{level}] {message}{RESET}")

# Function to check if NextDNS CLI is installed
def check_nextdns_installed():
    try:
        subprocess.run(["nextdns", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        log_and_print("NextDNS CLI is already installed.")
        return True
    except FileNotFoundError:
        log_and_print("NextDNS CLI is not installed.", level="ERROR")
        return False

# Function to install NextDNS CLI
def install_nextdns():
    log_and_print("Installing NextDNS CLI...")
    try:
        subprocess.run(
            "curl -sL https://nextdns.io/install | sudo sh",
            shell=True,
            check=True
        )
        log_and_print("NextDNS CLI installed successfully.")
    except subprocess.CalledProcessError as e:
        log_and_print(f"Installation failed: {e}", level="ERROR")


# Function to install miniupnpc (if required)
def install_miniupnpc():
    system = platform.system().lower()
    try:
        if system == "linux":
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Warning: Termux environment detected. You cannot access NextDNS in Termux.", level="ERROR")
                return
            else:
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    subprocess.run(["sudo", "apt", "install", "-y", "miniupnpc"], check=True)
                    log_and_print("MiniUPnP installed in Ubuntu/Debian.")
                elif "arch" in distro:
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "miniupnpc"], check=True)
                    log_and_print("MiniUPnP installed in Arch Linux.")
                elif "fedora" in distro or "redhat" in distro:
                    subprocess.run(["sudo", "dnf", "install", "-y", "miniupnpc"], check=True)
                    log_and_print("MiniUPnP installed in Fedora/RedHat.")
                else:
                    log_and_print("Unsupported Linux distribution for automatic installation of MiniUPnP.", level="ERROR")
        elif system == "darwin":
            if subprocess.run(["brew", "list", "miniupnpc"], capture_output=True).returncode != 0:
                subprocess.run(["brew", "install", "miniupnpc"], check=True)
                log_and_print("MiniUPnP installed on macOS.")
        else:
            log_and_print("MiniUPnP installation is not required for this system.", level="INFO")
    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install miniupnpc: {e}", level="ERROR")

# Function to configure DNS over TLS (DoT)
def configure_dot():
    log_and_print("Configuring DNS over TLS (DoT)...")
    try:
        # Assuming the user is using NextDNS with profile ID
        profile_id = input(f"{CYAN}Enter NextDNS Profile ID for DoT configuration: {RESET}")

        # Configure DNS over TLS
        subprocess.run(["sudo", "nextdns", "config", "dns-over-tls=true"], check=True)

        # Set the profile ID
        subprocess.run(["sudo", "nextdns", "config", f"profile={profile_id}"], check=True)

        log_and_print("DNS over TLS (DoT) configured successfully.")
    except subprocess.CalledProcessError as e:
        log_and_print(f"DNS over TLS (DoT) configuration failed: {e}", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred during DoT configuration: {e}", level="ERROR")


# Function to activate NextDNS with Profile ID
def activate_nextdns(profile_id):
    log_and_print(f"Activating NextDNS with Profile ID: {profile_id}...")
    try:
        subprocess.run(
            ["sudo", "nextdns", "activate", f"--profile={profile_id}"],
            check=True
        )
        log_and_print("NextDNS is now active.")
        configure_dot()  # Configure DNS over TLS (DoT) after activation
    except subprocess.CalledProcessError as e:
        log_and_print(f"Activation failed: {e}", level="ERROR")

# Function to deactivate NextDNS
def deactivate_nextdns():
    log_and_print("Deactivating NextDNS...")
    try:
        # Using sudo to ensure required privileges for deactivation
        subprocess.run(["sudo", "nextdns", "deactivate"], check=True)
        log_and_print("NextDNS is now deactivated.")
    except subprocess.CalledProcessError as e:
        log_and_print(f"Deactivation failed: {e}", level="ERROR")

# Function to verify DNS over TLS (DoT)
def verify_dot():
    log_and_print("Verifying DoT (DNS over TLS)...")
    try:
        # Fetching logs to verify DoT status
        result = subprocess.run(["sudo", "nextdns", "log"], stdout=subprocess.PIPE, text=True, check=True)
        if "DoT" in result.stdout:
            log_and_print("DoT is active and running.")
        else:
            log_and_print("DoT is not active. Please check your configuration.", level="WARNING")
    except subprocess.CalledProcessError as e:
        log_and_print(f"Unable to verify DoT: {e}", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred during DoT verification: {e}", level="ERROR")


# Function to view NextDNS logs
def view_nextdns_logs():
    log_and_print("Displaying NextDNS logs...")
    try:
        # Running the command to view logs
        subprocess.run(["sudo", "nextdns", "log"], check=True)
    except subprocess.CalledProcessError as e:
        log_and_print(f"Unable to display logs: {e}", level="ERROR")
    except FileNotFoundError:
        log_and_print("The 'nextdns' command was not found. Ensure NextDNS CLI is installed.", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred while displaying logs: {e}", level="ERROR")


# Function to detect environment and install necessary tools
def detect_environment_and_install():
    """Detect the environment and ensure necessary tools are available."""
    try:
        log_and_print("Detecting environment...", level="INFO")
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO")

        if system == "linux":
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Warning: Termux environment detected. You cannot access NextDNS in Termux.", level="ERROR")
                return
            else:
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing miniupnpc...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "miniupnpc"], check=True)
                    log_and_print("NextDNS is ready for DoT (DNS over TLS) configuration.")
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing miniupnpc...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "miniupnpc"], check=True)
                    log_and_print("NextDNS is ready for DoT (DNS over TLS) configuration.")
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing miniupnpc...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "miniupnpc"], check=True)
                    log_and_print("NextDNS is ready for DoT (DNS over TLS) configuration.")
                else:
                    log_and_print("Unsupported Linux distribution for automatic installation of MiniUPnP.", level="ERROR")
        elif system == "darwin":
            if subprocess.run(["brew", "list", "miniupnpc"], capture_output=True).returncode != 0:
                subprocess.run(["brew", "install", "miniupnpc"], check=True)
                log_and_print("NextDNS is ready for DoT (DNS over TLS) configuration.")
        else:
            log_and_print("MiniUPnP installation is not required for this system.", level="INFO")

        log_and_print("Environment setup and tool verification complete.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install necessary tools: {e}", level="ERROR")
        exit(1)

# Menu to manage NextDNS CLI
def main_menu():
    # Skip menu if Termux is detected
    if "com.termux" in os.environ.get("PREFIX", ""):
        return

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
            log_and_print("Invalid choice. Please try again.", level="ERROR")
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

# Entry point
if __name__ == "__main__":
    detect_environment_and_install()  # Detect environment and install necessary tools
    main_menu()