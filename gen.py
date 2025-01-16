import os
import ast
import sys
import subprocess
from importlib import import_module

# Define the directory where your Python scripts are located
scripts_directory = "tools"  # Update this to the directory containing your Python scripts

# List of standard Python libraries (can be enhanced further)
standard_libs = set(sys.builtin_module_names)  # Built-in modules are included here

# If needed, you can manually extend this list for modules that are part of the Python standard library but aren't "builtin"
# standard_libs.update({"datetime", "math", "os", "sys", ...})

def find_imports_in_script(script_path):
    """Scan a Python script for import statements."""
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)
    
    # Extract all imports
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
    
    return imports

def find_all_imports_in_directory(directory):
    """Find all imports in all Python scripts in a directory."""
    all_imports = set()
    
    # Walk through the scripts directory and find all Python files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                script_path = os.path.join(root, file)
                imports = find_imports_in_script(script_path)
                all_imports.update(imports)
    
    return all_imports

def filter_third_party_imports(imports):
    """Filter out the standard library modules from the imports."""
    return {pkg for pkg in imports if pkg not in standard_libs}

# Get all unique imports from all Python scripts in the tools directory
all_imports = find_all_imports_in_directory(scripts_directory)

# Filter out standard library imports
third_party_imports = filter_third_party_imports(all_imports)

# Write the third-party imports to requirements.txt
with open("requirements.txt", "w") as req_file:
    for package in sorted(third_party_imports):
        req_file.write(package + "\n")

print(f"Generated requirements.txt with {len(third_party_imports)} unique dependencies.")

# Install the dependencies listed in the requirements.txt
if third_party_imports:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
else:
    print("No third-party dependencies to install.")
