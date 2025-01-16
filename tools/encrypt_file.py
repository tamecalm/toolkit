import subprocess
import sys
from pathlib import Path

def encrypt_file():
    file_path = input("Enter the file path to encrypt: ").strip()
    if Path(file_path).is_file():
        try:
            subprocess.run(["gpg", "--symmetric", "--cipher-algo", "AES256", file_path], check=True)
            print(f"File encrypted successfully: {file_path}.gpg")
        except subprocess.CalledProcessError:
            print("Encryption failed. Ensure GPG is installed.")
    else:
        print("File does not exist. Please check the path.")

if __name__ == "__main__":
    encrypt_file()
