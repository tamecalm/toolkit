import os
import platform
import psutil
import subprocess
import shutil
import time

# Define theme colors
class Colors:
    DARK_GREEN = "\033[1;32m"
    DARK_CYAN = "\033[1;36m"
    DARK_RED = "\033[1;31m"
    DARK_BOLD = "\033[1m"
    DARK_RESET = "\033[0m"

# Logger class for color-coded logs and detailed file logging
class Logger:
    LOG_FILE = "data.log"

    @staticmethod
    def log(message, level="INFO"):
        color = {
            "INFO": Colors.DARK_CYAN,
            "WARNING": Colors.DARK_BOLD,
            "ERROR": Colors.DARK_RED
        }.get(level, Colors.DARK_RESET)

        formatted_message = f"{color}[{level}] {message}{Colors.DARK_RESET}"
        print(formatted_message)

        with open(Logger.LOG_FILE, "a") as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{level}] {message}\n")

# Detect the environment and distribution
class Environment:
    @staticmethod
    def detect():
        system = platform.system().lower()
        distro = platform.linux_distribution()[0].lower() if system == "linux" else None

        if system == "linux":
            if distro in ["ubuntu", "debian"]:
                return "debian"
            elif distro in ["fedora", "centos", "red hat"]:
                return "fedora"
            elif distro in ["arch", "manjaro"]:
                return "arch"
        elif system == "windows":
            return "windows"
        elif system == "darwin":
            return "macos"
        elif system == "android":
            return "termux"

        Logger.log("Unsupported environment detected!", "ERROR")
        return None

# Install dependencies based on environment
class DependencyInstaller:
    @staticmethod
    def install_dependencies():
        env = Environment.detect()
        if env == "debian":
            commands = ["sudo apt update", "sudo apt install -y python3-psutil"]
        elif env == "fedora":
            commands = ["sudo dnf update -y", "sudo dnf install -y python3-psutil"]
        elif env == "arch":
            commands = ["sudo pacman -Syu --noconfirm", "sudo pacman -S --noconfirm python-psutil"]
        elif env == "termux":
            commands = ["pkg update", "pkg install -y python3"]
        else:
            Logger.log("No dependency installation routine for this environment.", "WARNING")
            return

        for command in commands:
            try:
                subprocess.run(command, shell=True, check=True)
                Logger.log(f"Successfully executed: {command}")
            except subprocess.CalledProcessError as e:
                Logger.log(f"Command failed: {command} - {str(e)}", "ERROR")
                return

# Features implementation
class Toolkit:
    @staticmethod
    def cpu_memory_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        Logger.log(f"CPU Usage: {cpu_usage}%")
        Logger.log(f"Memory Usage: {memory_info.percent}%")

    @staticmethod
    def disk_usage():
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            Logger.log(f"Partition {partition.device} - Total: {usage.total / 1e9:.2f} GB, "
                       f"Used: {usage.used / 1e9:.2f} GB, Free: {usage.free / 1e9:.2f} GB")

    @staticmethod
    def network_info():
        addrs = psutil.net_if_addrs()
        for interface, addr_list in addrs.items():
            Logger.log(f"Interface: {interface}")
            for addr in addr_list:
                Logger.log(f"  {addr.family.name}: {addr.address}")

    @staticmethod
    def os_details():
        Logger.log(f"OS: {platform.system()}")
        Logger.log(f"Version: {platform.version()}")
        Logger.log(f"Architecture: {platform.architecture()[0]}")

    @staticmethod
    def battery_status():
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                Logger.log(f"Battery: {battery.percent}%")
                Logger.log(f"Charging: {'Yes' if battery.power_plugged else 'No'}")
            else:
                Logger.log("Battery information not available.", "WARNING")
        else:
            Logger.log("Battery information not supported on this platform.", "WARNING")

# Main menu
class MainMenu:
    @staticmethod
    def display():
        options = {
            "1": ("CPU and Memory Usage", Toolkit.cpu_memory_usage),
            "2": ("Disk Usage", Toolkit.disk_usage),
            "3": ("Network Information", Toolkit.network_info),
            "4": ("OS Details", Toolkit.os_details),
            "5": ("Battery Status", Toolkit.battery_status),
            "0": ("Exit", exit)
        }

        while True:
            print("\n" + Colors.DARK_BOLD + "Main Menu" + Colors.DARK_RESET)
            for key, (description, _) in options.items():
                print(f"  {key}. {description}")

            choice = input("\nSelect an option: ")
            action = options.get(choice)

            if action:
                _, func = action
                func()
            else:
                Logger.log("Invalid option!", "WARNING")

if __name__ == "__main__":
    DependencyInstaller.install_dependencies()
    MainMenu.display()
