import os
from pathlib import Path
import subprocess
import shutil
import re
import argparse

def run_command(cmd, verbose=True):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        if verbose:
            print(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command {cmd} failed with exit code {e.returncode}:")
        print(e.output)
        exit()


def check_conda_environment_exists(env_name):
    try:
        output = subprocess.check_output(['conda', 'info', '--envs'], universal_newlines=True)
        for line in output.split('\n'):
            if env_name in line:
                return True
        return False
    except subprocess.CalledProcessError:
        print("Error while checking conda environments.")
        return False

def is_conda_installed():
    try:
        # Run the 'conda --version' command and get the output
        result = subprocess.run(['conda', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False

def git_repos_has_remote(repo_path="."):
    try:
        result = subprocess.run(["git", "remote"], cwd=repo_path, capture_output=True, text=True)
        return bool(result.stdout.strip())
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_git_remote_url(remote_name):
    try:
        # Run the git remote get-url command and capture the output
        result = subprocess.run(["git", "remote", "get-url", remote_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return None

# Check if script is running from the same directory

script_path = Path(__file__).resolve()
current_directory = Path.cwd()

if current_directory != script_path.parent:
    print("Error: The script must be run within the same directory as the repository.")
    exit()

####################
### 0. Get input ###
####################

# Command-line arguments

parser = argparse.ArgumentParser(description="Boolean Argument Example")
parser.add_argument("-d", "--default", action="store_true", help="Use all default values")
parser.add_argument("-r", "--remote", default="", type=str, help="Remote repository")

args = parser.parse_args()
set_to_default = args.default

def get_input(prompt, default="", set_to_default=False):
    if not set_to_default:
        return input(prompt) or default
    else:
        return default

current_folder_name = Path(__file__).resolve().parent.stem

### Set parameters

new_project_name = get_input(f'Project name [{current_folder_name}]: ', default=current_folder_name, set_to_default=set_to_default)
description = get_input("Description: ", set_to_default=set_to_default)
python_version = get_input("Python version [3.10]: ", default='3.10', set_to_default=set_to_default)

create_conda_choice = get_input('Create conda environment [Y/n]? ', default='y', set_to_default=set_to_default).lower()
if create_conda_choice == 'y':
    conda_env_name = get_input(f"Conda env name [{Path.cwd().stem}]: ", default=Path.cwd().stem, set_to_default=set_to_default)
    if check_conda_environment_exists(conda_env_name):
        print(f"Error: Env {conda_env_name} exists.")
        exit()

    initialise_poetry_choice = get_input('Initialise poetry [Y/n]? ', default='y', set_to_default=set_to_default).lower()
    default_range = f'^{python_version},<3.13'
    python_version_range = get_input(f"Allowed Python version range [{default_range}]: ", default=default_range, set_to_default=set_to_default)
else:
    initialise_poetry_choice = 'n'

if not git_repos_has_remote():
    if not args.remote:
        remote_repository = get_input("Add remote repository (use ssh url) []: ", set_to_default=set_to_default)
    else:
        remote_repository = args.remote
elif git_repos_has_remote() and args.remote:
    print("Error: Can't specify remote when repository already has remote.")
    exit()
else:
    remote_repository = ''
if remote_repository:
    remote_branch = get_input("Remote branch [main]: ", default='main', set_to_default=set_to_default)

add_adu_tools_as_dev_dep = get_input(\
"""Choose to either add adu-tools as (a) a development dependency (b) a production dependency [A/b]
(note that development dependencies will not be included in pip packages): """, default='a', set_to_default=set_to_default).lower()
if add_adu_tools_as_dev_dep != 'a' and add_adu_tools_as_dev_dep != 'b':
    print("Poorly formatted answer")
    exit()

remove_script_choice = get_input('Remove this script [Y/n]? ', default='y', set_to_default=set_to_default).lower()

### Checks

if not is_conda_installed():
    print("Error: Must have anaconda installed.")
    exit()

# Check if the repository is currently that of adu-template-main.
# If yes, then remove .git and run git init
# If not, then do not remove .git

if get_git_remote_url('origin').strip() == 'git@github.com:Autonomy-Data-Unit/adu-template-main.git':
    remove_git = True
else:
    remove_git = False

################################################################################################
print("\n", "1. Change the project name from adu-template-main to the given project name", "\n")
################################################################################################

def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        filedata = file.read()

    # Replace the target string
    new_data = filedata.replace(old_string, new_string)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(new_data)

def is_text_file(filepath):
    try:
        # Open the file and read a portion of its contents
        with filepath.open('r', encoding='utf-8', errors='ignore') as f:
            content = f.read()  # Read first 512 characters
        # Check if the contents are printable
        return all(char.isprintable() or char.isspace() for char in content)
    except:
        return False

def replace_in_all_files(directory, old_string, new_string):
    # The following pattern matches all files in the given directory
    for file in Path(directory).rglob('*'):
        if file.is_file() and is_text_file(file):
            if file.resolve() == Path(__file__).resolve(): # Skip if it is this python file
                continue
            replace_string_in_file(file, old_string, new_string)

dir_path = '.'
old_project_name = 'adu-template-main'

pythonified_old_project_name = old_project_name.replace('-', '_')
pythonified_new_project_name = new_project_name.replace('-', '_')

replace_in_all_files(dir_path, old_project_name, new_project_name)
print(f'Changed all occurences of "{old_project_name}" to "{new_project_name}"')
replace_in_all_files(dir_path, pythonified_old_project_name, pythonified_new_project_name)
print(f'Changed all occurences of "{pythonified_old_project_name}" to "{pythonified_new_project_name}"')

# Change the module directory

# Define the path to the directory you want to rename
old_directory_path = Path(pythonified_old_project_name)
new_directory_name = pythonified_new_project_name
parent_directory = old_directory_path.parent
new_directory_path = parent_directory / new_directory_name
old_directory_path.rename(new_directory_path)
print(f'Module directory renamed from "{old_directory_path}" to "{new_directory_path}"')

##########################################
print("\n", "2. Set python version", "\n")
##########################################

replace_string_in_file('environment.yml', "python=3.10", f"python={python_version}")

################################################
print("\n", "3. Create conda environment", "\n")
################################################

if create_conda_choice == 'y':
    command = f"conda env create --file environment.yml --name {conda_env_name}"
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command {command} failed with exit code {e.returncode}:")
        print(e.output)
        exit()

    # Create envname file
    with open("envname", "w") as f:
        f.write(conda_env_name)

    print(f"Created environment {conda_env_name}")
    print(f"Environment name stored in ./envname")

#############################################
    print("\n", "4. Initialise poetry", "\n")
#############################################

    if initialise_poetry_choice == 'y':
        command = f"poetry init --no-interaction --name {new_project_name}"
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Command {command} failed with exit code {e.returncode}:")
            print(e.output)
            exit()

        print("Initialised poetry.")

############################################
    print("\n", "5. Set python range", "\n")
############################################

    file_path = 'pyproject.toml'
    with open(file_path, 'r') as file:
        filedata = file.read()

    def replace_value_after_equals(input_str, new_value):
        pattern = r'(?<=python = )"[^"]*"'
        replacement = f'"{new_value}"'
        return re.sub(pattern, replacement, input_str)

    new_data = replace_value_after_equals(filedata, python_version_range)

    with open(file_path, 'w') as file:
        file.write(new_data)

#########################################################
print("\n", "6. Set description in pyproject.toml", "\n")
#########################################################

if initialise_poetry_choice == 'y':
    file_path = 'pyproject.toml'
    with open(file_path, 'r') as file:
        filedata = file.read()

    def replace_value_after_equals(input_str, new_value):
        pattern = r'(?<=description = )"[^"]*"'
        replacement = f'"{new_value}"'
        return re.sub(pattern, replacement, input_str)

    new_data = replace_value_after_equals(filedata, description)

    with open(file_path, 'w') as file:
        file.write(new_data)

#######################################################################
    print("\n", "7. Add includes and excludes to pyproject.toml", "\n")
#######################################################################

    file_path = 'pyproject.toml'

    # Define the content to replace the section with
    append_content = \
"""include = [
    { path = "CHANGELOG.md", format = ["sdist", "wheel"] },
    { path = "README.md", format = ["sdist", "wheel"] }
]
exclude = ["%s/store/*"]
""" % new_project_name

    # Open the file
    with open(file_path, 'r') as file:
        pyproject_toml = file.read()

    re_pattern = r'(\[tool\.poetry\].*?)\n\n\[(?!tool\.poetry\])'

    # Extract the old content using regex
    old_content_match = re.search(re_pattern, pyproject_toml, flags=re.DOTALL)
    old_content = old_content_match.group(1) if old_content_match else None

    # Replace the section using regex
    new_pyproject_toml = re.sub(re_pattern, old_content + '\n' + append_content + '\n\n[', pyproject_toml, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(new_pyproject_toml)

####################################
print("\n", "8. CHANGELOG.md", "\n")
####################################

file_path = Path("CHANGELOG.md")
if file_path.is_file():
    file_path.unlink()
    print(f"Removed {file_path}")
else:
    print(f"{file_path} does not exist or is not a file")

source_path = Path("CHANGELOG_template.md")
destination_path = Path("CHANGELOG.md")
try:
    source_path.rename(destination_path)
    print(f"Moved {source_path} to {destination_path}")
except FileNotFoundError:
    print(f"{source_path} not found.")

if remove_git:
##################################################
    print("\n", "9. Delete the .git folder", "\n")
##################################################

    folder_path = '.git'

    if Path(folder_path).exists():
        try:
            shutil.rmtree(folder_path)
            print(f"Removed template .git folder")
        except Exception as e:
            print(f"Error: {e}")
            exit()
    else:
        print('Template .git is already removed')

###########################################
    print("\n", "10. Initialise git", "\n")
###########################################

    print("Initialising git")
    run_command("git init")




if remote_repository:
##################################################
    print("\n", "11. Add remote repository", "\n")
##################################################

    print('Adding remote:')
    run_command(f'git remote add origin {remote_repository}', verbose=True)
    run_command(f'git branch -M {remote_branch}', verbose=True)

    #if initial_commit == 'y':
    #    run_command(f'git add -A', verbose=True)
    #    run_command(f'git commit -m "Initial commit, using adu-template-main"', verbose=True)
    #    run_command(f'git push -u origin main')




####################################################################################
print("\n", "12. Add poetry sources and dependencies, and run poetry install", "\n")
####################################################################################

if initialise_poetry_choice == 'y':

    pip_packages_to_add = ['matplotlib', 'pandas', 'numpy']
    pip_dev_packages_to_add = ['jupyter', 'nbdev']
    adu_packages_to_add = ['adu-proj']
    adu_dev_packages_to_add = []

    if add_adu_tools_as_dev_dep == 'a':
        adu_dev_packages_to_add.append('adu-tools')
    else:
        adu_packages_to_add.append('adu-tools')

    run_command('poetry source add pypi')
    run_command('poetry source add --priority=supplemental adu https://pip.autonomy.work')

    if pip_packages_to_add: run_command(f'conda run -n {conda_env_name} poetry add {" ".join(pip_packages_to_add)}')
    if pip_dev_packages_to_add: run_command(f'conda run -n {conda_env_name} poetry add --group dev {" ".join(pip_dev_packages_to_add)}')
    if adu_packages_to_add: run_command(f'conda run -n {conda_env_name} poetry add --source adu {" ".join(adu_packages_to_add)}')
    if adu_dev_packages_to_add: run_command(f'conda run -n {conda_env_name} poetry add --source adu --group dev {" ".join(adu_dev_packages_to_add)}')

    run_command(f'conda run -n {conda_env_name} nbdev_export')
    run_command(f'conda run -n {conda_env_name} poetry install')



#############################################
    print("\n", "13. Initialise nbdev", "\n")
#############################################

    run_command(f'conda run -n {conda_env_name} nbdev_install_hooks')
    run_command(f'conda run -n {conda_env_name} nbdev_prepare')
    run_command(f'conda run -n {conda_env_name} nbdev_docs')


if remove_script_choice == 'y':
######################################################
    print("\n", "14. Remove prepare_project.py", "\n")
######################################################
    file_to_remove = Path('prepare_project.py')

    try:
        file_to_remove.unlink()
        print(f"File '{file_to_remove}' has been successfully removed.")
    except FileNotFoundError:
        print(f"Error: File '{file_to_remove}' not found.")
        exit()
    except Exception as e:
        print(f"Error: An error occurred while removing the file: {e}")
        exit()

###################################################
print("\n", "15. Cleaning up template files", "\n")
###################################################

files_to_delete = [
    Path(pythonified_new_project_name, 'tools', 'foo.py'),
    Path(pythonified_new_project_name, 'core', '01_first_steps.py'),
    Path(pythonified_new_project_name, 'cli', 'foo.py'),
]

for p in files_to_delete:
    print(f"Deleting {p}")
    p.unlink()

###############
### The End ###
###############


print("\nAll done!\n")

exit_message = f"""
You now need run the following

    adu-here

to activate the conda environment of the project.
"""

#if initial_commit != 'y':
#    exit_message += """
#5. To push to the remote, after adding and committing, run
#
#    git push -u origin main

#"""


exit_message += """
All dependencies should be added using `poetry add PACKAGE`. If for some reason this does not work, please install using conda and then add the dependency to the environment.yml.
"""

print(exit_message)
