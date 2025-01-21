import subprocess
import sys
import os
import platform
import psutil
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

# Install the psutil module
def install_psutil():
    """Install psutil module if not already installed."""
    try:
        import psutil
        log_and_print("psutil is already installed.", level="INFO")
    except ImportError:
        log_and_print("psutil not found, installing...", level="INFO")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        log_and_print("psutil has been installed.", level="INFO")

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
                subprocess.run(["pkg", "install", "-y", "procps"], check=True)
            else:
                # Check Linux distribution for package manager
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "procps", "net-tools"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "procps-ng", "net-tools"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "procps-ng", "net-tools"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install tools manually.", level="ERROR")
                    sys.exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected. Installing necessary tools via Homebrew...", level="INFO")
            subprocess.run(["brew", "install", "procps"], check=True)

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

def get_cpu_load():
    """Fetch CPU load using shell commands as a fallback."""
    try:
        result = subprocess.run(["cat", "/proc/loadavg"], capture_output=True, text=True, check=True)
        load_avg = result.stdout.split()[0]  # Get the 1-minute load average
        log_and_print(f"CPU Load Average (1 min): {load_avg}", level="INFO")
        print(Fore.GREEN + f"CPU Load Average (1 min): {load_avg}" + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to fetch CPU load average: {e}", level="ERROR")

def cpu_memory_usage():
    """Display real-time CPU and memory statistics."""
    log_and_print("Fetching CPU and memory usage...", level="INFO")
    try:
        if os.access('/proc/stat', os.R_OK):
            cpu_usage = psutil.cpu_percent(interval=1)
            log_and_print(f"CPU Usage: {cpu_usage}%", level="INFO")
            print(Fore.GREEN + f"CPU Usage: {cpu_usage}%" + Style.RESET_ALL)
        else:
            get_cpu_load()  # Use fallback method

        memory = psutil.virtual_memory()
        log_and_print(f"Memory Usage: {memory.percent}%", level="INFO")
        print(Fore.GREEN + f"Memory Usage: {memory.percent}%" + Style.RESET_ALL)
    except Exception as e:
        log_and_print(f"Error fetching CPU/Memory usage: {e}", level="ERROR")

def disk_usage():
    """Display disk usage information."""
    log_and_print("Fetching disk usage details...", level="INFO")
    disk = psutil.disk_usage('/')
    log_and_print(f"Total: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB", level="INFO")
    print(Fore.GREEN + f"Disk Usage -> Total: {disk.total / (1024 ** 3):.2f} GB, Used: {disk.used / (1024 ** 3):.2f} GB, Free: {disk.free / (1024 ** 3):.2f} GB" + Style.RESET_ALL)

def network_info():
    """Display network information."""
    log_and_print("Fetching network details...", level="INFO")
    try:
        if platform.system().lower() == "windows":
            command = ["ipconfig"]
        else:
            command = ["ifconfig"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        log_and_print(result.stdout, level="INFO")
        print(Fore.GREEN + result.stdout + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to fetch network details: {e}", level="ERROR")

def os_details():
    """Display OS version, kernel version, and architecture."""
    log_and_print("Fetching OS details...", level="INFO")
    os_name = platform.system()
    version = platform.version()
    architecture = platform.architecture()[0]
    log_and_print(f"OS: {os_name}, Version: {version}, Architecture: {architecture}", level="INFO")
    print(Fore.GREEN + f"OS: {os_name}, Version: {version}, Architecture: {architecture}" + Style.RESET_ALL)

def battery_status():
    """Display battery percentage, charging status, and health (if available)."""
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            log_and_print(f"Battery -> Percentage: {battery.percent}%, Charging: {'Yes' if battery.power_plugged else 'No'}", level="INFO")
            print(Fore.GREEN + f"Battery -> Percentage: {battery.percent}%, Charging: {'Yes' if battery.power_plugged else 'No'}" + Style.RESET_ALL)
        else:
            log_and_print("Battery details not available.", level="WARNING")
    else:
        log_and_print("Battery monitoring not supported on this system.", level="WARNING")

if __name__ == "__main__":
    log_and_print("System Info script started.", level="INFO")
    install_psutil()  # Ensure psutil is installed
    detect_environment_and_install()
    cpu_memory_usage()
    disk_usage()
    network_info()
    os_details()
    battery_status()
    log_and_print("System Info script finished.", level="INFO")
