import os
import platform
import subprocess
import logging
from colorama import Fore, Style
import miniupnpc

# Set up logging
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

# Install the miniupnpc module
def install_miniupnpc():
    """Install miniupnpc module if not already installed."""
    try:
        import miniupnpc
        log_and_print("miniupnpc is already installed.", level="INFO")
    except ImportError:
        log_and_print("miniupnpc not found, installing...", level="INFO")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "miniupnpc"])
        log_and_print("miniupnpc has been installed.", level="INFO")


def detect_environment_and_install():
    """Detect the environment and ensure necessary tools are available."""
    try:
        log_and_print("Detecting environment...", level="INFO")
        system = platform.system().lower()
        log_and_print(f"Operating System: {system}", level="INFO")

        if system == "linux":
            if "com.termux" in os.environ.get("PREFIX", ""):
                log_and_print("Termux environment detected. Installing miniupnpc...", level="INFO")
                subprocess.run(["pkg", "install", "-y", "miniupnpc"], check=True)
            else:
                distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
                if "ubuntu" in distro or "debian" in distro:
                    log_and_print("Ubuntu/Debian detected. Installing miniupnpc...", level="INFO")
                    subprocess.run(["sudo", "apt", "install", "-y", "miniupnpc"], check=True)
                elif "arch" in distro:
                    log_and_print("Arch Linux detected. Installing miniupnpc...", level="INFO")
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "miniupnpc"], check=True)
                elif "fedora" in distro or "redhat" in distro:
                    log_and_print("Fedora/RedHat detected. Installing miniupnpc...", level="INFO")
                    subprocess.run(["sudo", "dnf", "install", "-y", "miniupnpc"], check=True)
                else:
                    log_and_print("Unsupported Linux distribution. Please install miniupnpc manually.", level="ERROR")
                    exit(1)

        elif system == "darwin":
            log_and_print("macOS detected. Ensure miniupnpc is installed via Homebrew.", level="INFO")
            if subprocess.run(["brew", "list", "miniupnpc"], capture_output=True).returncode != 0:
                log_and_print("miniupnpc not found. Installing via Homebrew...", level="INFO")
                subprocess.run(["brew", "install", "miniupnpc"], check=True)

        elif system == "windows":
            log_and_print("Windows detected. Please ensure miniupnpc is installed via pip.", level="INFO")

        else:
            log_and_print("Unsupported system. Please install miniupnpc manually.", level="ERROR")
            exit(1)

        log_and_print("Environment setup and tool verification complete.", level="INFO")

    except subprocess.CalledProcessError as e:
        log_and_print(f"Failed to install necessary tools: {e}", level="ERROR")
        exit(1)

def setup_port_forwarding(local_port, external_port, protocol):
    """Set up port forwarding using UPnP."""
    try:
        log_and_print("Initializing UPnP client...", level="INFO")
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        discovered = upnp.discover()
        log_and_print(f"Discovered {discovered} UPnP devices.", level="INFO")

        upnp.selectigd()
        log_and_print(f"External IP: {upnp.externalipaddress()}", level="INFO")

        log_and_print(f"Adding port forwarding: {protocol} {external_port} -> {local_port}...", level="INFO")
        upnp.addportmapping(
            external_port, protocol, upnp.lanaddr, local_port, "Port Forwarding Setup", ""
        )
        log_and_print("Port forwarding rule added successfully.", level="INFO")

    except Exception as e:
        log_and_print(f"Failed to set up port forwarding: {e}", level="ERROR")

def remove_port_forwarding(external_port, protocol):
    """Remove a port forwarding rule."""
    try:
        log_and_print("Initializing UPnP client for removal...", level="INFO")
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        discovered = upnp.discover()
        log_and_print(f"Discovered {discovered} UPnP devices.", level="INFO")

        upnp.selectigd()
        log_and_print(f"External IP: {upnp.externalipaddress()}", level="INFO")

        log_and_print(f"Removing port forwarding: {protocol} {external_port}...", level="INFO")
        upnp.deleteportmapping(external_port, protocol)
        log_and_print("Port forwarding rule removed successfully.", level="INFO")

    except Exception as e:
        log_and_print(f"Failed to remove port forwarding: {e}", level="ERROR")

if __name__ == "__main__":
    log_and_print("Port Forwarding Setup started.", level="INFO")

    install_miniupnpc()

    detect_environment_and_install()

    print(Fore.CYAN + "=== Port Forwarding Setup ===" + Style.RESET_ALL)
    action = input("Enter action (add/remove): ").strip().lower()
    if action not in ["add", "remove"]:
        log_and_print("Invalid action provided. Exiting.", level="ERROR")
    else:
        protocol = input("Enter protocol (TCP/UDP): ").strip().upper()
        external_port = int(input("Enter external port: ").strip())
        if action == "add":
            local_port = int(input("Enter local port: ").strip())
            setup_port_forwarding(local_port, external_port, protocol)
        elif action == "remove":
            remove_port_forwarding(external_port, protocol)

    log_and_print("Port Forwarding Setup finished.", level="INFO")