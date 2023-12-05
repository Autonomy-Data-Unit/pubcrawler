import os, pkgutil, importlib, sys
from .. import log

def run_all():
    # Run all scripts in this folder in alphanumerical order
    scripts = list(f"{__package__}.{module_name}" for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
    scripts = sorted(scripts)
    for s in scripts:
        log.info(f"{'#' * (len(s)+4)}")
        log.info(f"# {s} #")
        log.info(f"{'#' * (len(s)+4)}")
        if s in sys.modules:
            module = importlib.import_module(s)
            importlib.reload(module)
        else:
            importlib.import_module(s)