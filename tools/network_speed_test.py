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

def log_and_print(message, level="INFO"):
    """Log a message and print it to the console."""
    level = level.upper()
    log_func = getattr(logging, level.lower(), logging.info)
    log_func(message)
    print(message)

# Check Dependency
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
    """Detect the environment and install necessary dependencies."""
    try:
        logging.info("Detecting environment...")

        # Detect platform
        system = platform.system().lower()
        logging.info(f"Operating System: {system}")

        if system == "linux":
            # Check for Termux environment
            if "com.termux" in os.environ.get("PREFIX", ""):
                logging.info("Termux environment detected. Installing dependencies...")
                subprocess.run(["pkg", "install", "-y", "python", "pip"], check=True)
            else:
                # Check Linux distribution using lsb_release
                try:
                    distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                except FileNotFoundError:
                    logging.error("'lsb_release' command not found. Unable to determine Linux distribution.")
                    sys.exit(1)

                logging.info(f"Detected Linux Distribution: {distro}")

                if "ubuntu" in distro or "debian" in distro:
                    logging.info("Ubuntu/Debian detected. Installing dependencies...")
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-pip"], check=True)
                elif "arch" in distro:
                    logging.info("Arch Linux detected. Installing dependencies...")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "python", "python-pip"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    logging.info("Fedora/RedHat detected. Installing dependencies...")
                    subprocess.run(["sudo", "dnf", "install", "-y", "python3", "python3-pip"], check=True)
                else:
                    logging.error("Unsupported Linux distribution. Please install dependencies manually.")
                    sys.exit(1)

        elif system == "darwin":
            # macOS
            logging.info("macOS detected. Installing dependencies via Homebrew...")
            subprocess.run(["brew", "install", "python", "pip"], check=True)

        elif system == "windows":
            # Windows
            logging.info("Windows detected. Checking for Python installation...")
            if not shutil.which("python") and not shutil.which("python3"):
                logging.error("Python not found. Please download and install it from https://www.python.org/.")
                sys.exit(1)

        else:
            logging.error("Unsupported system. Please install dependencies manually.")
            sys.exit(1)

        logging.info("Dependencies installed successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install dependencies: {e}")
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
    detect_environment_and_install()
    check_dependency()
    network_speed_test()
