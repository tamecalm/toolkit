import os
import configparser
import time
import sys

# Configuration file path
CONFIG_FILE = os.path.expanduser("~/.nextdns_config")

# ANSI escape sequences for "hacking" colors
RESET = "\033[0m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"

# Load configuration from the config file
def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"{RED}[ERROR] Config file not found: {CONFIG_FILE}{RESET}")
        exit(1)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

# Loading animation
def loading_animation(message):
    for i in range(3):
        sys.stdout.write(f"\r{CYAN}{message}{'.' * (i + 1)}{RESET}")
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r")

# Load configuration
config = load_config()
API_KEY = config.get("DEFAULT", "API_KEY")

def activate_nextdns(profile_name):
    if profile_name not in config.sections():
        print(f"{RED}[ERROR] Profile '{profile_name}' not found in config file.{RESET}")
        return

    profile = config[profile_name]
    dot_url = profile.get("DOT_URL")
    ipv6_1 = profile.get("IPV6_1")
    ipv6_2 = profile.get("IPV6_2")

    print(f"{GREEN}[INFO] Activating NextDNS profile: {profile_name}...{RESET}")
    
    # Configure DNS-over-TLS
    try:
        resolv_conf = "/data/data/com.termux/files/usr/etc/resolv.conf"
        with open(resolv_conf, "w") as f:
            f.write(f"nameserver {dot_url}\n")
            f.write(f"nameserver {ipv6_1}\n")
            f.write(f"nameserver {ipv6_2}\n")
        loading_animation("Configuring DNS-over-TLS (DoT)")
        print(f"{GREEN}[SUCCESS] DNS-over-TLS (DoT) configured.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] DoT configuration error: {e}{RESET}")
        return

def test_dns():
    print(f"{CYAN}[INFO] Testing NextDNS configuration...{RESET}")
    loading_animation("Testing DNS setup")
    try:
        response = os.system("ping -c 1 google.com")
        if response == 0:
            print(f"{GREEN}[SUCCESS] NextDNS is active and working.{RESET}")
        else:
            print(f"{RED}[ERROR] DNS test failed.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] DNS test error: {e}{RESET}")

def list_profiles():
    print(f"{CYAN}[INFO] Listing all profiles...{RESET}")
    for section in config.sections():
        print(f"{GREEN}  - {section}{RESET}")

def check_query_usage():
    print(f"{CYAN}[INFO] Fetching query usage stats...{RESET}")
    loading_animation("Fetching stats")
    url = "https://api.nextdns.io/profiles"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for profile in data:
                print(f"{GREEN}Profile: {profile['id']}{RESET}")
                print(f"  Queries Used: {profile['queries']}")
                print(f"  Queries Left: {profile['remainingQueries']}")
        else:
            print(f"{RED}[ERROR] Failed to fetch stats: {response.status_code} - {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Query usage error: {e}{RESET}")

def main_menu():
    while True:
        os.system("clear")
        print(f"{GREEN}--- NextDNS Manager ---{RESET}".center(50))
        print(f"{CYAN}Use this tool to configure, test, and manage NextDNS.{RESET}".center(50))
        print(f"{CYAN}Ensure the configuration file is correctly set up before proceeding.{RESET}".center(50))
        print(f"\n{GREEN}Main Menu:{RESET}")
        print(f"{CYAN}1. Activate NextDNS Profile{RESET}")
        print(f"{CYAN}2. Test DNS Configuration{RESET}")
        print(f"{CYAN}3. List All Profiles{RESET}")
        print(f"{CYAN}4. Check Query Usage Stats{RESET}")
        print(f"{CYAN}5. Exit{RESET}")
        
        choice = input(f"\n{GREEN}Select an option: {RESET}")
        
        if choice == "1":
            profile_name = input(f"{CYAN}Enter profile name to activate: {RESET}")
            activate_nextdns(profile_name)
        elif choice == "2":
            test_dns()
        elif choice == "3":
            list_profiles()
        elif choice == "4":
            check_query_usage()
        elif choice == "5":
            print(f"{GREEN}Exiting...{RESET}")
            break
        else:
            print(f"{RED}[ERROR] Invalid choice. Please try again.{RESET}")
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main_menu()