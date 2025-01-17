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
                subprocess.run(["pkg", "install", "-y", "traceroute"], check=True)
            else:
                # Check Linux distribution for package manager
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "traceroute"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "traceroute"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "traceroute"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install tools manually.", level="ERROR")
                    sys.exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected. Installing necessary tools via Homebrew...", level="INFO")
            subprocess.run(["brew", "install", "traceroute"], check=True)

        elif system == "windows":
            # Windows
            log_and_print("Windows detected. No additional installation required.", level="INFO")

        else:
            log_and_print("Unsupported system. Please install tools manually.", level="ERROR")
            sys.exit(1)

        log_and_print("Environment detected and tools installed successfully.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install necessary tools: {e}", level="ERROR")
        sys.exit(1)

def traceroute(host):
    """Perform a traceroute to the specified host."""
    log_and_print(f"Starting traceroute to {host}...", level="INFO")
    try:
        # Determine the platform and select the appropriate traceroute command
        system = platform.system().lower()
        if system == "windows":
            command = ["tracert", host]
        else:
            command = ["traceroute", host]

        log_and_print(f"Executing command: {' '.join(command)}", level="INFO")

        # Execute the traceroute command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        # Print and log the traceroute output
        log_and_print("Traceroute results:", level="INFO")
        print(Fore.GREEN + output + Style.RESET_ALL)
        logging.info(output)

    except subprocess.CalledProcessError as e:
        log_and_print(f"Traceroute failed: {e}", level="ERROR")
    except FileNotFoundError:
        log_and_print("Traceroute command not found. Ensure it is installed on your system.", level="ERROR")
    except Exception as e:
        log_and_print(f"An unexpected error occurred: {e}", level="ERROR")

if __name__ == "__main__":
    log_and_print("Traceroute Utility started.", level="INFO")
    detect_environment_and_install()
    
    # Get user input for the host
    target_host = input(Fore.CYAN + "Enter the host to trace (e.g., google.com): " + Style.RESET_ALL).strip()
    
    if not target_host:
        log_and_print("No host provided. Exiting.", level="ERROR")
    else:
        traceroute(target_host)

    log_and_print("Traceroute Utility finished.", level="INFO")
