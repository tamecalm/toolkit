import subprocess

def network_speed_test():
    try:
        subprocess.run(["speedtest-cli", "--simple"], check=True)
    except subprocess.CalledProcessError:
        print("Speed test failed. Ensure speedtest-cli is installed.")

if __name__ == "__main__":
    network_speed_test()
