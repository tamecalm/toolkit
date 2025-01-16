import subprocess

def port_scanner():
    target = input("Enter the target IP or hostname: ").strip()
    try:
        subprocess.run(["nmap", target], check=True)
    except subprocess.CalledProcessError:
        print("Port scanning failed. Ensure nmap is installed.")

if __name__ == "__main__":
    port_scanner()
