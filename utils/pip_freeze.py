import subprocess
import os

# Function to run pip freeze and get the list of installed packages
def get_installed_packages():
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').splitlines()

# Function to read a list from a file
def read_list_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

# Function to write a list to a file
def write_list_to_file(filename, list_to_write):
    with open(filename, 'w') as file:
        for item in list_to_write:
            file.write("%s\n" % item)

# Get the list of installed packages using pip freeze
installed_packages = get_installed_packages()

# Read the list of required packages from "requirements.txt"
required_packages = read_list_from_file('../requirements.txt')

# Create a dictionary from the installed packages for quick version lookup
version_dict = {pkg.split("==")[0]: pkg for pkg in installed_packages if "==" in pkg}

# Create the new list by matching required packages with their versions
new_requirements = [version_dict[pkg] for pkg in required_packages if pkg in version_dict]

# Rename the original "requirements.txt" to "requirements.txt.old"
os.rename('../requirements.txt', '../requirements.txt.old')

# Write the new list to "requirements.txt"
write_list_to_file('../requirements.txt', new_requirements)

# # Rename the new file to "requirements.txt"
# os.rename('requirements.txt', 'requirements.txt')

print("Operation completed successfully.")