import subprocess
import sys
import shutil
import logging

# Configure logging
logging.basicConfig(
    filename="err.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
