import subprocess
import sys
import os
import logging
from colorama import Fore, Style

# Set up logging configuration
LOG_FILE = "err.log"
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

def detect_environment():
    """Detect the platform environment (Termux, Ubuntu, etc.)."""
    log_and_print("[*] Detecting environment...", level="INFO")
    try:
        if os.path.exists("/data/data/com.termux/files/usr/bin/termux-info"):
            return "termux"

        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                os_release = f.read().lower()
                if "ubuntu" in os_release or "debian" in os_release:
                    return "ubuntu"
                elif "fedora" in os_release:
                    return "fedora"
                elif "arch" in os_release:
                    return "arch"

        uname_output = subprocess.check_output(["uname", "-a"], text=True).lower()
        if "android" in uname_output:
            return "termux"

        return "unknown"
    except Exception as e:
        log_and_print(f"[!] Failed to detect environment: {e}", level="ERROR")
        sys.exit(1)

def install_dependencies_for_environment(environment):
    """Install dependencies based on the detected environment."""
    try:
        if environment == "termux":
            log_and_print("[*] Installing dependencies for Termux...", level="INFO")
            subprocess.run(["pkg", "install", "-y", "termux-tools", "wireless-tools"], check=True)
            log_and_print("[*] Termux dependencies installed successfully.", level="INFO")
        elif environment in ["ubuntu", "debian"]:
            log_and_print("[*] Installing dependencies for Ubuntu/Debian...", level="INFO")
            subprocess.run(["sudo", "apt", "install", "-y", "iw", "wireless-tools"], check=True)
            log_and_print("[*] Ubuntu/Debian dependencies installed successfully.", level="INFO")
        elif environment == "fedora":
            log_and_print("[*] Installing dependencies for Fedora...", level="INFO")
            subprocess.run(["sudo", "dnf", "install", "-y", "iw", "wireless-tools"], check=True)
            log_and_print("[*] Fedora dependencies installed successfully.", level="INFO")
        elif environment == "arch":
            log_and_print("[*] Installing dependencies for Arch Linux...", level="INFO")
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "iw", "wireless_tools"], check=True)
            log_and_print("[*] Arch Linux dependencies installed successfully.", level="INFO")
        else:
            log_and_print("[!] Unsupported environment. Please install Wi-Fi tools manually.", level="ERROR")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        log_and_print(f"[!] Failed to install dependencies for {environment}: {e}", level="ERROR")
        sys.exit(1)

def parse_termux_output(output):
    """Parse Wi-Fi scan output from Termux."""
    try:
        import json
        networks = json.loads(output)
        for idx, network in enumerate(networks, 1):
            print(Fore.GREEN + f"{idx}. SSID: {network.get('SSID', 'Unknown')}, Strength: {network.get('RSSI', 'N/A')} dBm" + Style.RESET_ALL)
            log_and_print(f"Network {idx}: {network}", level="INFO")
    except json.JSONDecodeError as e:
        log_and_print(f"[!] Failed to parse Termux output: {e}", level="ERROR")

def parse_iwlist_output(output):
    """Parse Wi-Fi scan output from iwlist."""
    networks = []
    for line in output.split("\n"):
        if "ESSID" in line:
            networks.append(line.strip())
    for idx, network in enumerate(networks, 1):
        print(Fore.GREEN + f"{idx}. {network}" + Style.RESET_ALL)
        log_and_print(f"Network {idx}: {network}", level="INFO")

def wifi_analyzer():
    """Scan for Wi-Fi networks and display results."""
    log_and_print("[*] Starting Wi-Fi scan...", level="INFO")

    try:
        environment = detect_environment()
        command = ["termux-wifi-scaninfo"] if environment == "termux" else ["sudo", "iwlist", "wlan0", "scan"]
        log_and_print(f"[*] Running command: {' '.join(command)}", level="INFO")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output = result.stdout.strip()

        if not output:
            log_and_print("[!] No Wi-Fi networks found. Ensure Wi-Fi is enabled.", level="WARNING")
        elif environment == "termux":
            parse_termux_output(output)
        else:
            parse_iwlist_output(output)

    except subprocess.CalledProcessError as e:
        log_and_print(f"[!] Wi-Fi scan failed: {e}", level="ERROR")
    except Exception as e:
        log_and_print(f"[!] An unexpected error occurred: {e}", level="ERROR")
        sys.exit(1)

if __name__ == "__main__":
    log_and_print("[*] Wi-Fi Analyzer script started.", level="INFO")

    # Step 1: Detect environment and install dependencies
    environment = detect_environment()
    log_and_print(f"[*] Detected environment: {environment}", level="INFO")
    install_dependencies_for_environment(environment)

    # Step 2: Run Wi-Fi Analyzer
    wifi_analyzer()

    log_and_print("[*] Wi-Fi Analyzer script finished.", level="INFO")
