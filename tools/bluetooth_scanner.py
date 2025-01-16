import subprocess

def bluetooth_scanner():
    try:
        subprocess.run(["termux-bluetooth-scan"], check=True)
    except subprocess.CalledProcessError:
        print("Bluetooth scanning failed. Ensure Termux and required permissions are set.")

if __name__ == "__main__":
    bluetooth_scanner()
