# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/const.ipynb.

# %% auto 0
__all__ = ['root_path', 'store_path', 'logs_path', 'data_path', 'pre_output_path', 'output_path', 'figs_path', 'url', 'file_type']

# %% ../nbs/const.ipynb 4
from pathlib import Path
import pubcrawler as proj

# %% ../nbs/const.ipynb 6
root_path = Path(proj.__file__).parent.resolve().as_posix()
store_path = Path(root_path, 'store').as_posix()
logs_path = Path(store_path, 'logs').as_posix()
data_path = Path(store_path, 'data').as_posix()
pre_output_path = Path(store_path, 'pre_output').as_posix()
output_path = Path(store_path, 'output').as_posix()
figs_path = Path(store_path, 'output/figs').as_posix()

# %% ../nbs/const.ipynb 7
# Create the directories, if they don't exist already
Path(store_path).mkdir(exist_ok=True)
Path(logs_path).mkdir(exist_ok=True)
Path(logs_path, 'csv').mkdir(exist_ok=True)
Path(data_path).mkdir(exist_ok=True)
Path(pre_output_path).mkdir(exist_ok=True)
Path(output_path).mkdir(exist_ok=True)
Path(figs_path).mkdir(exist_ok=True)

# %% ../nbs/const.ipynb 8
url = 'https://autonomy.work/'
file_type = 'pdf'
