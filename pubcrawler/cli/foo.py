# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/cli/cli_02_foo.ipynb.

# %% auto 0
__all__ = ['cmd_name', 'cmd_description', 'parser', 'args', 'const_dict', 'log_name', 'store_log_path', 'a', 'b']

# %% ../../nbs/cli/cli_02_foo.ipynb 4
import sys

import pubcrawler as proj
from .. import const, log, utils, tools
import adu_proj.utils as adutils

# %% ../../nbs/cli/cli_02_foo.ipynb 5
def main(): pass # This is necessary for console_scripts

# %% ../../nbs/cli/cli_02_foo.ipynb 9
if adutils.cli.is_interactive():
    sys.argv = ['', # First element is not parsed by argparse
                '4', '6']

# %% ../../nbs/cli/cli_02_foo.ipynb 11
cmd_name = 'cli.foo'
cmd_description = "Add up two numbers"

# %% ../../nbs/cli/cli_02_foo.ipynb 12
## Define arg parser
parser = adutils.cli.get_default_arg_parser()
parser.description = cmd_description
parser.prog = cmd_name
parser.add_argument("number1", help="Number 1")
parser.add_argument("number2", help="Number 2")
parser.set_defaults(store_log=False) # Don't store log by default

## Parse args and adjust settings
args = parser.parse_args()
const_dict = adutils.cli.set_const_args(const, args)
log_name = cmd_name if not args.log_name else args.log_name
store_log_path = const.logs_path if args.store_log else None
log.settings(log_name, store_log_path=store_log_path, print_log=args.print_log)

## Output all values in const into the log
adutils.cli.log_all_const()

## Run command with settings
a, b = args.number1, args.number2
log.info(f'The sum of {a} and {b} is {tools.foo(a,b)}')
