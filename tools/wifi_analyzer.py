import subprocess

def wifi_analyzer():
    try:
        subprocess.run(["termux-wifi-scaninfo"], check=True)
    except subprocess.CalledProcessError:
        print("Wi-Fi analysis failed. Ensure Termux and required permissions are set.")

if __name__ == "__main__":
    wifi_analyzer()
