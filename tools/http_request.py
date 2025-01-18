import subprocess
import platform
import logging
import os
import sys
import json
from colorama import Fore, Style
import requests  # Ensure this is installed via detect_environment_and_install

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
                subprocess.run(["pkg", "install", "-y", "python"], check=True)
            else:
                # Check Linux distribution for package manager
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "python3-pip"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "python-pip"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing necessary tools...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "python3-pip"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install tools manually.", level="ERROR")
                    exit(1)

        elif system == "darwin":
            # macOS
            log_and_print("macOS detected. Ensuring necessary tools are available...", level="INFO")
            if subprocess.run(["which", "python3"], capture_output=True).returncode != 0:
                log_and_print("Python3 is not installed. Please install it manually.", level="ERROR")
                exit(1)

        elif system == "windows":
            # Windows
            log_and_print("Windows detected. Ensuring pip is installed...", level="INFO")
            subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], check=True)

        else:
            log_and_print("Unsupported system. Please install tools manually.", level="ERROR")
            exit(1)

        # Ensure requests library is installed
        log_and_print("Checking for 'requests' library...", level="INFO")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        log_and_print("Environment detected and tools verified successfully.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install necessary tools: {e}", level="ERROR")
        exit(1)

def print_notes():
    """Display usage notes for the script."""
    notes = """
    Welcome to the HTTP Request Tester!
    
    Instructions:
    1. Use the menu to select the type of HTTP request you want to send (GET, POST, PUT, DELETE).
    2. For POST and PUT requests, you can specify a JSON body.
    3. Ensure you provide a valid URL (e.g., https://jsonplaceholder.typicode.com/posts).
    4. The script will display the response status and content.
    5. Logs are saved in 'data.log'.

    Let's get started!
    """
    print(Fore.GREEN + notes + Style.RESET_ALL)

def send_get_request(url):
    """Send a GET request."""
    try:
        log_and_print(f"Sending GET request to {url}...", level="INFO")
        response = requests.get(url)
        log_and_print(f"Response Status: {response.status_code}", level="INFO")
        log_and_print(f"Response Content:\n{response.text}", level="INFO")
        print(Fore.GREEN + f"Response Status: {response.status_code}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Response Content:\n{response.text}" + Style.RESET_ALL)
    except Exception as e:
        log_and_print(f"GET request failed: {e}", level="ERROR")

def send_post_request(url, data):
    """Send a POST request."""
    try:
        log_and_print(f"Sending POST request to {url} with data: {data}", level="INFO")
        response = requests.post(url, json=data)
        log_and_print(f"Response Status: {response.status_code}", level="INFO")
        log_and_print(f"Response Content:\n{response.text}", level="INFO")
        print(Fore.GREEN + f"Response Status: {response.status_code}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Response Content:\n{response.text}" + Style.RESET_ALL)
    except Exception as e:
        log_and_print(f"POST request failed: {e}", level="ERROR")

def send_put_request(url, data):
    """Send a PUT request."""
    try:
        log_and_print(f"Sending PUT request to {url} with data: {data}", level="INFO")
        response = requests.put(url, json=data)
        log_and_print(f"Response Status: {response.status_code}", level="INFO")
        log_and_print(f"Response Content:\n{response.text}", level="INFO")
        print(Fore.GREEN + f"Response Status: {response.status_code}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Response Content:\n{response.text}" + Style.RESET_ALL)
    except Exception as e:
        log_and_print(f"PUT request failed: {e}", level="ERROR")

def send_delete_request(url):
    """Send a DELETE request."""
    try:
        log_and_print(f"Sending DELETE request to {url}...", level="INFO")
        response = requests.delete(url)
        log_and_print(f"Response Status: {response.status_code}", level="INFO")
        log_and_print(f"Response Content:\n{response.text}", level="INFO")
        print(Fore.GREEN + f"Response Status: {response.status_code}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Response Content:\n{response.text}" + Style.RESET_ALL)
    except Exception as e:
        log_and_print(f"DELETE request failed: {e}", level="ERROR")

def main_menu():
    """Main menu for HTTP Request Tester."""
    while True:
        print(Fore.CYAN + "\nHTTP Request Tester Menu" + Style.RESET_ALL)
        print("1. Send GET Request")
        print("2. Send POST Request")
        print("3. Send PUT Request")
        print("4. Send DELETE Request")
        print("5. Notes")
        print("6. Exit")
        
        choice = input(Fore.CYAN + "Select an option (1-6): " + Style.RESET_ALL).strip()
        
        if choice == "1":
            url = input(Fore.CYAN + "Enter the URL for GET request: " + Style.RESET_ALL).strip()
            send_get_request(url)
        elif choice == "2":
            url = input(Fore.CYAN + "Enter the URL for POST request: " + Style.RESET_ALL).strip()
            data = input(Fore.CYAN + "Enter JSON data for POST request: " + Style.RESET_ALL).strip()
            send_post_request(url, json.loads(data))
        elif choice == "3":
            url = input(Fore.CYAN + "Enter the URL for PUT request: " + Style.RESET_ALL).strip()
            data = input(Fore.CYAN + "Enter JSON data for PUT request: " + Style.RESET_ALL).strip()
            send_put_request(url, json.loads(data))
        elif choice == "4":
            url = input(Fore.CYAN + "Enter the URL for DELETE request: " + Style.RESET_ALL).strip()
            send_delete_request(url)
        elif choice == "5":
            print_notes()
        elif choice == "6":
            log_and_print("Exiting HTTP Request Tester.", level="INFO")
            break
        else:
            log_and_print("Invalid choice. Please select a valid option.", level="WARNING")

if __name__ == "__main__":
    log_and_print("HTTP Request Tester started.", level="INFO")
    detect_environment_and_install()
    print_notes()
    main_menu()
    log_and_print("HTTP Request Tester finished.", level="INFO")
