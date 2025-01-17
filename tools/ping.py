import os
import subprocess
import platform
import logging
from colorama import Fore, Style

# Set up logging configuration
LOG_FILE = "data.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message, level="INFO"):
    """Log a message to file and print to terminal."""
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
    """Detect the environment and install required tools if necessary."""
    try:
        log_and_print("Detecting environment...", level="INFO")

        # Detect platform
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO")

        if system == "linux":
            # Check for Termux environment
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Termux environment detected. Installing necessary tools...", level="INFO")
                subprocess.run(["pkg", "install", "-y", "inetutils"], check=True)
            else:
                # Check Linux distribution for package manager
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "iputils-ping"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "iputils"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "iputils"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install tools manually.", level="ERROR")
                    exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected. Ensuring necessary tools are available...", level="INFO")
            if subprocess.run(["which", "ping"], capture_output=True).returncode != 0:
                log_and_print("Ping utility not found. Please install it manually.", level="ERROR")
                exit(1)

        elif system == "windows":
            # Windows
            log_and_print("Windows detected. No additional installation required.", level="INFO")

        else:
            log_and_print("Unsupported system. Please install tools manually.", level="ERROR")
            exit(1)

        log_and_print("Environment detected and tools verified successfully.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install necessary tools: {e}", level="ERROR")
        exit(1)

def ping_host(host, count=4):
    """Ping a host to test reachability."""
    try:
        log_and_print(f"Pinging host: {host} with {count} requests...", level="INFO")

        # Determine the ping command based on platform
        system = platform.system().lower()
        if system == "windows":
            command = ["ping", "-n", str(count), host]
        else:
            command = ["ping", "-c", str(count), host]

        # Execute the ping command
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            log_and_print(f"Ping successful for host: {host}", level="INFO")
            print(Fore.GREEN + result.stdout + Style.RESET_ALL)
        else:
            log_and_print(f"Ping failed for host: {host}", level="ERROR")
            print(Fore.RED + result.stderr + Style.RESET_ALL)

    except FileNotFoundError:
        log_and_print("Ping utility not found. Please ensure it is installed on your system.", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred: {e}", level="ERROR")

if __name__ == "__main__":
    log_and_print("Ping Utility started.", level="INFO")
    
    detect_environment_and_install()
    
    # Get user input for the host
    target_host = input(Fore.CYAN + "Enter the host to ping (e.g., google.com): " + Style.RESET_ALL).strip()
    if not target_host:
        log_and_print("No host provided. Exiting.", level="ERROR")
    else:
        ping_host(target_host)

    log_and_print("Ping Utility finished.", level="INFO")