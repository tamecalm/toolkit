import psutil
import shutil

def system_health():
    print("CPU Usage:")
    print(psutil.cpu_percent(interval=1), "%")
    
    print("\nMemory Usage:")
    mem = psutil.virtual_memory()
    print(f"Total: {mem.total // (1024 ** 2)} MB, Used: {mem.used // (1024 ** 2)} MB, Free: {mem.free // (1024 ** 2)} MB")
    
    print("\nStorage Usage:")
    total, used, free = shutil.disk_usage("/")
    print(f"Total: {total // (1024 ** 3)} GB, Used: {used // (1024 ** 3)} GB, Free: {free // (1024 ** 3)} GB")

if __name__ == "__main__":
    system_health()
