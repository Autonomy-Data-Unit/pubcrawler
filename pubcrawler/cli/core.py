# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/cli/cli_01_core.ipynb.

# %% auto 0
__all__ = ['cmd_name', 'cmd_description', 'parser', 'args', 'const_dict', 'log_name', 'store_log_path']

# %% ../../nbs/cli/cli_01_core.ipynb 4
import sys
import ast

import pubcrawler as proj
from .. import const, log, utils, tools, core
import adu_proj.utils as adutils

# %% ../../nbs/cli/cli_01_core.ipynb 5
def main(): pass # This is necessary for console_scripts

# %% ../../nbs/cli/cli_01_core.ipynb 9
if adutils.cli.is_interactive():
    sys.argv = ['', # First element is not parsed by argparse
                '--const-str', 'figs_path=~/figs',
                '--log-name', 'test_log_name',
                '--no-store-log',
                '--print-log']

# %% ../../nbs/cli/cli_01_core.ipynb 11
cmd_name = 'cli.core'
cmd_description = "Execute package."

# %% ../../nbs/cli/cli_01_core.ipynb 12
## Define arg parser
parser = adutils.cli.get_default_arg_parser()
parser.description = cmd_description

## Parse args and adjust settings
args = parser.parse_args()
const_dict = adutils.cli.set_const_args(const, args)
log_name = cmd_name if not args.log_name else args.log_name
store_log_path = const.logs_path if args.store_log else None
log.settings(log_name, store_log_path=store_log_path, print_log=args.print_log)

## Output all values in const into the log
adutils.cli.log_all_const()

## Run command with settings
if const.selected_scripts:
    if isinstance(const.selected_scripts, list):
        core.run_selected_scripts(const.selected_scripts)
    elif isinstance(const.selected_scripts, str):
        selected_scripts = ast.literal_eval(const.selected_scripts)
        core.run_selected_scripts(selected_scripts)    
    else:
        print(f"{const.selected_scripts} was neither string nor list")
else:
    ## Run command with settings
    core.run_all()
