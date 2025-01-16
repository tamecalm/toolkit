import time
import subprocess

def schedule_task():
    command = input("Enter the command to schedule: ").strip()
    interval = int(input("Enter the interval in minutes: ").strip())
    print(f"Scheduling '{command}' every {interval} minutes...")
    
    while True:
        subprocess.run(command, shell=True)
        time.sleep(interval * 60)

if __name__ == "__main__":
    schedule_task()
