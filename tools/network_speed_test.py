import os
import sys
import subprocess
import platform
import shutil
import logging

# Configure logging
logging.basicConfig(
    filename="data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# Configure Logging 2

def log_and_print(message, level="INFO"):
    """Log a message and print it to the console."""
    level = level.upper()
    log_func = getattr(logging, level.lower(), logging.info)
    log_func(message)
    print(message)

# Check Dependecy
def check_dependency():
    """Ensure that speedtest-cli is installed."""
    if not shutil.which("speedtest-cli"):
        print("Dependency 'speedtest-cli' not found. Installing it now...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "speedtest-cli"], check=True)
            logging.info("speedtest-cli successfully installed.")
        except subprocess.CalledProcessError as e:
            error_msg = "Failed to install speedtest-cli. Please try installing it manually."
            logging.error(error_msg)
            print(f"\033[1;31m{error_msg}\033[0m")
            sys.exit(1)

def detect_environment_and_install():
    """Detect the environment and install nmap if necessary."""
    try:
        log_and_print("Detecting environment...", level="INFO")

        # Detect platform
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO")

        if system == "linux":
            # Check for Termux environment
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Termux environment detected. Installing nmap...", level="INFO")
                subprocess.run(["pkg", "install", "-y", "nmap"], check=True)
            else:
                # Check Linux distribution using lsb_release
                try:
                    distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                except FileNotFoundError:
                    log_and_print("'lsb_release' command not found. Unable to determine Linux distribution.", level="ERROR")
                    sys.exit(1)

                log_and_print(f"Detected Linux Distribution: {distro}", level="INFO")

                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing nmap...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "nmap"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing nmap...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "nmap"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing nmap...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "nmap"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install nmap manually.", level="ERROR")
                    sys.exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected. Installing nmap via Homebrew...", level="INFO")
            subprocess.run(["brew", "install", "nmap"], check=True)

        elif system == "windows":
            # Windows
            log_and_print("Windows detected. Checking for nmap installation...", level="INFO")
            if not shutil.which("nmap"):
                log_and_print("nmap not found. Please download and install it from https://nmap.org/download.html", level="ERROR")
                sys.exit(1)

        else:
            log_and_print("Unsupported system. Please install nmap manually.", level="ERROR")
            sys.exit(1)

        log_and_print("nmap installed successfully.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install nmap: {e}", level="ERROR")
        sys.exit(1)

def network_speed_test():
    """Run the network speed test."""
    try:
        print("\033[1;34mRunning network speed test...\033[0m")
        result = subprocess.run(["speedtest-cli", "--simple"], text=True, capture_output=True, check=True)
        print("\033[1;32mSpeed Test Results:\033[0m")
        print(result.stdout)
        logging.info("Speed test successful.")
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        error_msg = "Speed test failed. Ensure you have an active internet connection."
        print(f"\033[1;31m{error_msg}\033[0m")
        logging.error(f"{error_msg}\n{e}")
    except Exception as e:
        error_msg = "An unexpected error occurred during the speed test."
        print(f"\033[1;31m{error_msg}\033[0m")
        logging.error(f"{error_msg}\n{e}")

if __name__ == "__main__":
    # Display a simple interface
    print("\033[1;36m" + "=" * 40 + "\033[0m")
    print("\033[1;36m     Network Speed Test Utility\033[0m")
    print("\033[1;36m" + "=" * 40 + "\033[0m")

    # Check dependencies and run the test
    check_dependency()
    network_speed_test()
