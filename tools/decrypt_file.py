import subprocess
import sys
from pathlib import Path

def decrypt_file():
    file_path = input("Enter the file path to decrypt: ").strip()
    if Path(file_path).is_file():
        try:
            subprocess.run(["gpg", "--decrypt", file_path], check=True)
        except subprocess.CalledProcessError:
            print("Decryption failed. Ensure GPG is installed.")
    else:
        print("File does not exist. Please check the path.")

if __name__ == "__main__":
    decrypt_file()
