import psutil
import shutil
import os
import logging
from colorama import Fore, Style

# Configure logging
LOG_FILE = "system_health.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_dependencies():
    """Ensure required dependencies are installed."""
    try:
        __import__('colorama')
    except ImportError:
        print("Installing missing dependency: colorama")
        os.system("pip install colorama")


def format_size(bytes, unit="MB"):
    """Convert bytes to human-readable format."""
    factor = 1024 ** 2 if unit == "MB" else 1024 ** 3
    return bytes // factor

def display_system_health():
    """Displays system health information neatly."""
    try:
        print(Fore.CYAN + Style.BRIGHT + "\nSystem Health Check".center(50, "=") + Style.RESET_ALL)

        # CPU Usage
        print(Fore.YELLOW + "\nCPU Usage:" + Style.RESET_ALL)
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"{cpu_usage}%")
        logging.info(f"CPU Usage: {cpu_usage}%")

        # Memory Usage
        print(Fore.YELLOW + "\nMemory Usage:" + Style.RESET_ALL)
        mem = psutil.virtual_memory()
        mem_info = f"Total: {format_size(mem.total)} MB, Used: {format_size(mem.used)} MB, Free: {format_size(mem.available)} MB"
        print(mem_info)
        logging.info(f"Memory Usage: {mem_info}")

        # Storage Usage
        print(Fore.YELLOW + "\nStorage Usage:" + Style.RESET_ALL)
        total, used, free = shutil.disk_usage("/")
        storage_info = (f"Total: {format_size(total, 'GB')} GB, Used: {format_size(used, 'GB')} GB, Free: {format_size(free, 'GB')} GB")
        print(storage_info)
        logging.info(f"Storage Usage: {storage_info}")

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(Fore.RED + error_message + Style.RESET_ALL)
        logging.error(error_message)

if __name__ == "__main__":
    check_dependencies()
    display_system_health()
