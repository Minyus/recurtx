import sys
import traceback
from pathlib import Path
from typing import List, Union


def get_exception_msg():
    return "".join(traceback.format_exception(*sys.exc_info()))


def upath(
    path: str,
):
    if isinstance(path, str) and path.startswith("~"):
        path = str(Path.home()) + path[1:]
    if isinstance(path, str) and path.startswith("."):
        path = str(Path.cwd()) + path[1:]
    return path


def subprocess_run(
    script: Union[str, List[str]],
    verbose: bool = True,
):
    if verbose:
        sys.stdout.write(r">>> " + script + "\n")

        from time import sleep

        sleep(0.2)

    import subprocess

    shell = isinstance(script, str)
    return subprocess.run(script, shell=shell)
