import os
import configparser
import requests
import subprocess

# Configuration file path
CONFIG_FILE = os.path.expanduser("~/.nextdns_config")

# Load configuration from the config file
def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERROR] Config file not found: {CONFIG_FILE}")
        exit(1)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

# Load configuration
config = load_config()

# API key from the config file
API_KEY = config.get("DEFAULT", "API_KEY")

def activate_nextdns(profile_name):
    if profile_name not in config.sections():
        print(f"[ERROR] Profile '{profile_name}' not found in config file.")
        return

    profile = config[profile_name]
    doh_url = profile.get("DOH_URL")
    dot_url = profile.get("DOT_URL")
    ipv6_1 = profile.get("IPV6_1")
    ipv6_2 = profile.get("IPV6_2")

    print(f"[INFO] Activating NextDNS profile: {profile_name}...")
    
    # Configure DNS-over-TLS
    try:
        resolv_conf = "/data/data/com.termux/files/usr/etc/resolv.conf"
        with open(resolv_conf, "w") as f:
            f.write(f"nameserver {dot_url}\n")
            f.write(f"nameserver {ipv6_1}\n")
            f.write(f"nameserver {ipv6_2}\n")
        print("[SUCCESS] DNS-over-TLS (DoT) configured.")
    except Exception as e:
        print(f"[ERROR] DoT configuration error: {e}")

    # Test DoH
    try:
        print("[INFO] Testing DNS-over-HTTPS (DoH)...")
        response = requests.get(doh_url, headers={"Authorization": f"Bearer {API_KEY}"})
        if response.status_code == 200:
            print("[SUCCESS] DNS-over-HTTPS (DoH) is active.")
        else:
            print(f"[ERROR] DoH setup failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] DoH configuration error: {e}")

def test_dns():
    print("[INFO] Testing NextDNS configuration...")
    try:
        response = requests.get("https://my.nextdns.io")
        if response.status_code == 200:
            print("[SUCCESS] NextDNS is active and working.")
        else:
            print(f"[ERROR] DNS test failed: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] DNS test error: {e}")

def list_profiles():
    print("[INFO] Listing all profiles...")
    for section in config.sections():
        print(f"  - {section}")

def main_menu():
    while True:
        print("\n--- NextDNS Manager ---")
        print("1. Activate NextDNS Profile")
        print("2. Test DNS Configuration")
        print("3. List All Profiles")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            profile_name = input("Enter profile name to activate: ")
            activate_nextdns(profile_name)
        elif choice == "2":
            test_dns()
        elif choice == "3":
            list_profiles()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()