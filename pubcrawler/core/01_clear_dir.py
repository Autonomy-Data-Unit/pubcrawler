# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/core/01_clean-Copy1.ipynb.

# %% auto 0
__all__ = ['delete_all_files_from_dir']

# %% ../../nbs/core/01_clean-Copy1.ipynb 4
import pubcrawler as proj
from .. import const, log, utils, tools
import adu_proj.utils as adutils

# %% ../../nbs/core/01_clean-Copy1.ipynb 5
import os
import shutil

# %% ../../nbs/core/01_clean-Copy1.ipynb 6
def delete_all_files_from_dir(target_dir):
    # Ensure the directory exists
    if not os.path.exists(target_dir):
        print("The specified directory does not exist.")
        return
    # Loop through all the files and subdirectories in the target directory
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        try:
            # If it's a directory, use shutil.rmtree to delete it and its contents
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            # If it's a file, use os.unlink (or os.remove) to delete it
            else:
                os.unlink(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

# %% ../../nbs/core/01_clean-Copy1.ipynb 7
delete_all_files_from_dir(const.pre_output_path)
