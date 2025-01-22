import os
import ast
import sys
import subprocess
import sysconfig
import time
import platform
import distro

# Define the directory where your Python scripts are located
scripts_directory = "tools"  # Update this to the directory containing your Python scripts

# List of standard Python libraries (can be enhanced further)
standard_libs = set(sys.builtin_module_names)  # Built-in modules are included here

# Extend with more standard library modules
standard_libs.update({
    "datetime", "math", "os", "sys", "logging", "json", "socket", "platform", "unittest", "collections", "subprocess",
    "argparse", "csv", "hashlib", "http", "itertools", "pickle", "random", "re", "struct", "time", "uuid", "shutil", "zipfile"
    # Add any additional modules from Python's standard library here
})

# List of problematic packages to skip during installation
problematic_packages = {"miniupnpc"}  # Add known problematic packages here

# Ethical hacker theme style for output
def print_banner():
    os.system("clear")  # Clear the terminal screen
    print("\033[92m")
    print("=" * 60)
    print("   🔍  Python Dependency Analyzer & Installer  💻")
    print("=" * 60)
    print("\033[0m")

def progress_bar(total, current, length=50):
    filled = int(length * current // total)
    bar = "█" * filled + "-" * (length - filled)
    print(f"\r[{bar}] {current}/{total}", end="", flush=True)

def log_error(message):
    with open("data.log", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {message}\n")

def log_info(message):
    with open("data.log", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - INFO: {message}\n")

def find_imports_in_script(script_path):
    """Scan a Python script for import statements."""
    try:
        with open(script_path, "r") as file:
            tree = ast.parse(file.read(), filename=script_path)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
        return imports
    except Exception as e:
        log_error(f"Error parsing script {script_path}: {e}")
        return set()

def find_all_imports_in_directory(directory):
    """Find all imports in all Python scripts in a directory."""
    all_imports = set()
    scripts = []
    for root, _, files in os.walk(directory):
        scripts.extend([os.path.join(root, file) for file in files if file.endswith(".py")])

    total_scripts = len(scripts)
    for i, script_path in enumerate(scripts, start=1):
        imports = find_imports_in_script(script_path)
        all_imports.update(imports)
        progress_bar(total_scripts, i)
        time.sleep(0.05)  # Simulate progress
    print()  # Move to the next line after the progress bar
    return all_imports

def filter_third_party_imports(imports):
    """Filter out the standard library modules from the imports."""
    return {pkg for pkg in imports if pkg not in standard_libs}

def detect_environment_and_install(package):
    """Install a package based on the detected environment."""
    try:
        if "termux" in os.getenv("PREFIX", ""):
            subprocess.check_call(["pkg", "install", "-y", package])
        elif "ubuntu" in distro.id() or "debian" in distro.id():
            subprocess.check_call(["sudo", "apt", "install", "-y", f"python3-{package}"])
        elif platform.system() == "Windows":
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        error_message = f"Failed to install {package}: {e}"
        print(f"\n\033[91m{error_message}\033[0m")
        log_error(error_message)

def install_requirements():
    """Install dependencies from requirements.txt."""
    try:
        print("\033[93mInstalling dependencies...\033[0m")
        with open("requirements.txt", "r") as req_file:
            requirements = [line.strip() for line in req_file if line.strip()]

        total_requirements = len(requirements)
        for i, package in enumerate(requirements, start=1):
            progress_bar(total_requirements, i)

            if package in problematic_packages:
                warning_message = f"Skipping {package} due to known issues."
                print(f"\n\033[93m{warning_message}\033[0m")
                log_info(warning_message)
                continue

            detect_environment_and_install(package)
            time.sleep(0.1)
        print("\033[92mDependencies installed successfully!\033[0m")
        log_info("Dependencies installed successfully.")
    except Exception as e:
        error_message = f"An unexpected error occurred during installation: {e}"
        print(f"\033[91m{error_message}\033[0m")
        log_error(error_message)

# Main execution flow
print_banner()

try:
    all_imports = find_all_imports_in_directory(scripts_directory)
    third_party_imports = filter_third_party_imports(all_imports)
    incorrect_imports = third_party_imports.intersection(standard_libs)
    if incorrect_imports:
        log_info(f"Found built-in modules mistakenly added: {incorrect_imports}")
        third_party_imports -= incorrect_imports

    with open("requirements.txt", "w") as req_file:
        for package in sorted(third_party_imports):
            req_file.write(package + "\n")

    print(f"\033[94mGenerated requirements.txt with {len(third_party_imports)} unique dependencies.\033[0m")
    log_info(f"Generated requirements.txt with {len(third_party_imports)} unique dependencies.")

    if third_party_imports:
        install_requirements()
    else:
        print("\033[92mNo third-party dependencies to install.\033[0m")
        log_info("No third-party dependencies to install.")
except Exception as e:
    error_message = f"An unexpected error occurred: {e}"
    print(f"\033[91m{error_message}\033[0m")
    log_error(error_message)

print("\033[92mTask completed. Check data.log for detailed logs.\033[0m")
