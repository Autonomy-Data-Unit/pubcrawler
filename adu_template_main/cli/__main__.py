import os
import sys

def list_submodules(directory):
    """List all submodules in a directory."""
    
    # List all files that end with .py
    files = [f for f in os.listdir(directory) if f.endswith(".py")]
    
    # Exclude __init__.py and __main__.py
    files = [f for f in files if f not in ("__init__.py", "__main__.py")]
    
    # Return module names without the .py extension
    return [os.path.splitext(f)[0] for f in files]

# Assuming the __main__.py is in the same directory as the submodules
current_directory = os.path.dirname(os.path.abspath(__file__))

submodules = list_submodules(current_directory)

print("Commands:")
for submodule in submodules:
    print(f"   {submodule}")