import subprocess
import sys
import os
import platform
import logging
from shutil import which
from colorama import Fore, Style

# Set up logging configuration
LOG_FILE = "data.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message, level="INFO"):
    """Log message to file and print to terminal."""
    if level == "ERROR":
        logging.error(message)
        print(Fore.RED + f"[ERROR] {message}" + Style.RESET_ALL)
    elif level == "WARNING":
        logging.warning(message)
        print(Fore.YELLOW + f"[WARNING] {message}" + Style.RESET_ALL)
    else:
        logging.info(message)
        print(Fore.CYAN + f"[INFO] {message}" + Style.RESET_ALL)

def detect_environment_and_install():
    """Detect the environment and install Wi-Fi tools if necessary."""
    try:
        log_and_print("Detecting environment...", level="INFO")

        # Detect platform
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO")

        if system == "linux":
            # Check for Termux environment
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Termux environment detected. Installing Wi-Fi tools...", level="INFO")
                subprocess.run(["pkg", "install", "-y", "termux-tools"], check=True)
            else:
                # Check Linux distribution for package manager
                distro_name = distro.name().lower()  # Get the distribution name using the distro module
                if "ubuntu" in distro_name or "debian" in distro_name:
                    log_and_print("Ubuntu/Debian detected. Installing Wi-Fi tools...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "iw", "wireless-tools"], check=True)
                elif "arch" in distro_name:
                    log_and_print("Arch Linux detected. Installing Wi-Fi tools...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "iw", "wireless_tools"], check=True)
                elif "fedora" in distro_name or "redhat" in distro_name:
                    log_and_print("Fedora/RedHat detected. Installing Wi-Fi tools...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "iw", "wireless-tools"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install Wi-Fi tools manually.", level="ERROR")
                    sys.exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected. Installing Wi-Fi tools via Homebrew...", level="INFO")
            subprocess.run(["brew", "install", "wireless-tools"], check=True)

        elif system == "windows":
            # Windows
            log_and_print("Windows detected. Checking for Wi-Fi tools installation...", level="INFO")
            if not which("netsh"):
                log_and_print("Wi-Fi tools not found. Please install them manually.", level="ERROR")
                sys.exit(1)

        else:
            log_and_print("Unsupported system. Please install Wi-Fi tools manually.", level="ERROR")
            sys.exit(1)

        log_and_print("Wi-Fi tools installed successfully.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install Wi-Fi tools: {e}", level="ERROR")
        sys.exit(1)

def wifi_scan_windows():
    """Scan for Wi-Fi networks on Windows."""
    try:
        command = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        log_and_print(f"Running command: {' '.join(command)}", level="INFO")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output = result.stdout.strip()

        if not output:
            log_and_print("No Wi-Fi networks found. Ensure Wi-Fi is enabled.", level="WARNING")
        else:
            log_and_print("Wi-Fi networks found:", level="INFO")
            print(Fore.GREEN + output + Style.RESET_ALL)
            log_and_print(output, level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Wi-Fi scan failed: {e}", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred: {e}", level="ERROR")
        sys.exit(1)

def wifi_analyzer():
    """Scan for Wi-Fi networks and display results."""
    log_and_print("Starting Wi-Fi scan...", level="INFO")

    try:
        system = platform.system().lower()
        if system == "windows":
            wifi_scan_windows()
        elif system == "linux":
            command = ["termux-wifi-scaninfo"] if "com.termux" in os.environ.get("PREFIX", "") else ["iwlist", "scanning"]
            log_and_print(f"Running command: {' '.join(command)}", level="INFO")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            output = result.stdout.strip()

            if not output:
                log_and_print("No Wi-Fi networks found. Ensure Wi-Fi is enabled.", level="WARNING")
            else:
                log_and_print("Wi-Fi networks found:", level="INFO")
                print(Fore.GREEN + output + Style.RESET_ALL)
                log_and_print(output, level="INFO")
        else:
            log_and_print("Unsupported system for Wi-Fi scanning.", level="ERROR")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        log_and_print(f"Wi-Fi scan failed: {e}", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred: {e}", level="ERROR")
        sys.exit(1)

if __name__ == "__main__":
    log_and_print("Wi-Fi Analyzer script started.", level="INFO")

    # Step 1: Detect environment and install dependencies
    detect_environment_and_install()

    # Step 2: Run Wi-Fi Analyzer
    wifi_analyzer()

    log_and_print("Wi-Fi Analyzer script finished.", level="INFO")
