import subprocess
import logging
import sys
import os
from colorama import Fore, Style

# Set up logging configuration
LOG_FILE = "port_scanner.log"
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

def detect_terminal_and_install():
    """Detect the terminal environment and install nmap."""
    try:
        # Detect the terminal environment (e.g., Termux, Ubuntu, etc.)
        terminal = os.getenv('TERM_PROGRAM', 'Unknown').lower()
        log_and_print(f"[*] Detected terminal: {terminal}", level="INFO")

        if 'termux' in terminal:
            # Termux installation
            log_and_print("[*] Termux detected. Installing nmap...", level="INFO")
            subprocess.run(["pkg", "install", "-y", "nmap"], check=True)
        elif 'ubuntu' in terminal or 'debian' in terminal:
            # Ubuntu/Debian installation
            log_and_print("[*] Ubuntu/Debian detected. Installing nmap...", level="INFO")
            subprocess.run(["sudo", "apt", "install", "-y", "nmap"], check=True)
        elif 'arch' in terminal:
            # Arch Linux installation
            log_and_print("[*] Arch Linux detected. Installing nmap...", level="INFO")
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "nmap"], check=True)
        elif 'fedora' in terminal:
            # Fedora installation
            log_and_print("[*] Fedora detected. Installing nmap...", level="INFO")
            subprocess.run(["sudo", "dnf", "install", "-y", "nmap"], check=True)
        else:
            log_and_print("[!] Unknown terminal. Please install nmap manually.", level="ERROR")
            sys.exit(1)

        log_and_print("[*] nmap installed successfully.", level="INFO")
    except subprocess.CalledProcessError as e:
        log_and_print(f"[!] Failed to install nmap: {e}", level="ERROR")
        sys.exit(1)

def port_scanner():
    """Port scanning functionality."""
    log_and_print("[*] Starting port scan...", level="INFO")
    
    # Get target IP/hostname and ports
    target = input("Enter the target IP or hostname: ").strip()
    ports = input("Enter port range (e.g., 22-80, 443, 8080): ").strip()

    try:
        # Execute nmap command with user-defined target and port range
        command = ["nmap", target, "-p", ports]
        log_and_print(f"[*] Running command: {' '.join(command)}", level="INFO")
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Check the result of the scan
        if result.stdout:
            print(Fore.GREEN + "\nScan Results:" + Style.RESET_ALL)
            print(result.stdout)
            log_and_print(f"[*] Scan completed for {target} on ports {ports}.", level="INFO")
        else:
            log_and_print("[!] No results found.", level="WARNING")

    except subprocess.CalledProcessError as e:
        log_and_print(f"[!] Port scan failed: {e}", level="ERROR")
    except Exception as e:
        log_and_print(f"[!] An unexpected error occurred: {e}", level="ERROR")
        sys.exit(1)

if __name__ == "__main__":
    # Step 1: Detect terminal and install nmap if necessary
    detect_terminal_and_install()

    # Step 2: Run Port Scanner
    port_scanner()

    log_and_print("[*] Port scanning script finished.", level="INFO")