import os
import sys
import glob
import inspect

# Get the current file path and name
current_file = inspect.getframeinfo(inspect.currentframe()).filename
print()
print(f"Current file: {current_file}")

venv_path = os.path.dirname(sys.executable)
print(f"Current virtual environment path: {venv_path}")

executable_path = sys.executable
print(f"Current Python executable path: {executable_path}")

# Check if the Python executable is part of a VSCode workspace
vscode_workspace_path = None
for folder in glob.glob(os.path.join(os.path.expanduser("~"), ".vscode")):
    for workspace_file in glob.glob(os.path.join(folder, "*.code-workspace")):
        with open(workspace_file, "r") as f:
            workspace_data = f.read()
            if venv_path in workspace_data:
                vscode_workspace_path = os.path.dirname(workspace_file)
                break

if vscode_workspace_path:
    print(f"The virtual environment is part of the VSCode workspace: {vscode_workspace_path}")
else:
    print("The virtual environment is not part of a VSCode workspace")
