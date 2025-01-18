import subprocess
import platform
import logging
import os
import sys
import json
import time
import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Logging setup
LOG_FILE = "http_request_tester.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message, level="INFO", hacker_style=False):
    """Log a message to file and optionally print to terminal in hacker style."""
    if hacker_style:
        message = Fore.GREEN + message + Style.RESET_ALL
    if level == "ERROR":
        logging.error(message)
        print(Fore.RED + f"[ERROR] {message}" + Style.RESET_ALL)
    elif level == "WARNING":
        logging.warning(message)
        print(Fore.YELLOW + f"[WARNING] {message}" + Style.RESET_ALL)
    else:
        logging.info(message)
        print(Fore.CYAN + f"[INFO] {message}" + Style.RESET_ALL)

def loading_animation(message):
    """Display a loading or fetching animation with percentage."""
    for i in range(1, 101):
        sys.stdout.write(f"\r{Fore.GREEN}{message}... {i}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.03)
    print()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_python_version():
    """Check if Python is installed and satisfies the required version."""
    try:
        log_and_print("Checking Python installation...", level="INFO")
        version = subprocess.check_output(["python3", "--version"], text=True).strip()
        log_and_print(f"Python version detected: {version}", level="INFO")
    except FileNotFoundError:
        log_and_print("Python is not installed. Installing Python...", level="INFO")
        loading_animation("Installing Python")
        subprocess.run(["sudo", "apt", "install", "-y", "python3"], check=True)
        log_and_print("Python installed successfully.", level="INFO")

def check_requests_library():
    """Check if the requests library is installed and up-to-date."""
    try:
        log_and_print("Checking if 'requests' library is installed...", level="INFO")
        import requests
        log_and_print("Requests library is already installed.", level="INFO")
    except ImportError:
        log_and_print("'Requests' library not found. Installing...", level="INFO")
        loading_animation("Installing 'requests' library")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        log_and_print("'Requests' library installed successfully.", level="INFO")

def detect_environment_and_install():
    """Detect the environment and install required tools if necessary."""
    try:
        log_and_print("Detecting environment...", level="INFO", hacker_style=True)

        # Detect platform
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO", hacker_style=True)

        if system == "linux":
            # Check for Termux environment
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Termux environment detected.", level="INFO", hacker_style=True)
                loading_animation("Installing required tools")
                subprocess.run(["pkg", "install", "-y", "python"], check=True)
            else:
                # Check Linux distribution for package manager
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected.", level="INFO", hacker_style=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected.", level="INFO", hacker_style=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected.", level="INFO", hacker_style=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install tools manually.", level="ERROR")
                    exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected.", level="INFO", hacker_style=True)

        elif system == "windows":
            # Windows
            log_and_print("Windows detected.", level="INFO", hacker_style=True)

        else:
            log_and_print("Unsupported system. Please install tools manually.", level="ERROR")
            exit(1)

        check_python_version()
        check_requests_library()

        loading_animation("Setting up the environment")
        log_and_print("Environment detected and tools verified successfully.", level="INFO")
        clear_screen()

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install necessary tools: {e}", level="ERROR")
        exit(1)

def send_get_request(url):
    """Send a GET request."""
    log_and_print(f"Sending GET request to {url}...", level="INFO")
    response = requests.get(url)
    print(Fore.GREEN + f"Response: {response.status_code}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Content: {response.text}" + Style.RESET_ALL)

def send_post_request(url, data):
    """Send a POST request."""
    log_and_print(f"Sending POST request to {url} with data {data}...", level="INFO")
    response = requests.post(url, json=data)
    print(Fore.GREEN + f"Response: {response.status_code}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Content: {response.text}" + Style.RESET_ALL)

def send_put_request(url, data):
    """Send a PUT request."""
    log_and_print(f"Sending PUT request to {url} with data {data}...", level="INFO")
    response = requests.put(url, json=data)
    print(Fore.GREEN + f"Response: {response.status_code}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Content: {response.text}" + Style.RESET_ALL)

def send_delete_request(url):
    """Send a DELETE request."""
    log_and_print(f"Sending DELETE request to {url}...", level="INFO")
    response = requests.delete(url)
    print(Fore.GREEN + f"Response: {response.status_code}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Content: {response.text}" + Style.RESET_ALL)

def main_menu():
    """Main menu for the script."""
    while True:
        print(Fore.GREEN + """
        ******************************
        * HTTP Request Tester        *
        ******************************
        1. Send GET Request
        2. Send POST Request
        3. Send PUT Request
        4. Send DELETE Request
        5. Exit
        ******************************
        """ + Style.RESET_ALL)

        choice = input(Fore.GREEN + "Select an option (1-5): " + Style.RESET_ALL).strip()
        if choice == "1":
            url = input(Fore.GREEN + "Enter the URL: " + Style.RESET_ALL).strip()
            send_get_request(url)
        elif choice == "2":
            url = input(Fore.GREEN + "Enter the URL: " + Style.RESET_ALL).strip()
            data = json.loads(input(Fore.GREEN + "Enter the JSON data: " + Style.RESET_ALL).strip())
            send_post_request(url, data)
        elif choice == "3":
            url = input(Fore.GREEN + "Enter the URL: " + Style.RESET_ALL).strip()
            data = json.loads(input(Fore.GREEN + "Enter the JSON data: " + Style.RESET_ALL).strip())
            send_put_request(url, data)
        elif choice == "4":
            url = input(Fore.GREEN + "Enter the URL: " + Style.RESET_ALL).strip()
            send_delete_request(url)
        elif choice == "5":
            log_and_print("Exiting script. Goodbye!", level="INFO")
            break
        else:
            log_and_print("Invalid choice. Please try again.", level="WARNING")

if __name__ == "__main__":
    detect_environment_and_install()
    main_menu()
