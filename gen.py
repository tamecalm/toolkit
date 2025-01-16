import os
import ast

# Define the directory where your Python scripts are located
scripts_directory = "tools"  # Update this to the directory containing your Python scripts

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

# Get all unique imports from all Python scripts in the tools directory
all_imports = find_all_imports_in_directory(scripts_directory)

# Write the imports to requirements.txt
with open("requirements.txt", "w") as req_file:
    for package in sorted(all_imports):
        req_file.write(package + "\n")

print(f"Generated requirements.txt with {len(all_imports)} unique dependencies.")
