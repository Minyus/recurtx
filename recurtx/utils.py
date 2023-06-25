import sys
import traceback
from pathlib import Path
from typing import List, Set, Union


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
        sys.stdout.write(r">>> " + str(script) + "\n")

        from time import sleep

        sleep(0.2)

    import subprocess

    shell = isinstance(script, str)
    return subprocess.run(script, shell=shell)


def stdout_lines(text: str):
    if not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)


def infer_type(
    type: str,
    path: str,
    supported_types: Set[str],
    polars: bool = False,
):
    if isinstance(type, str) and type:
        _type = type
        _type = _type.replace("md", "markdown")
        if polars:
            _type = _type.replace("jsonl", "ndjson")
        assert _type in supported_types, (
            _type + " not in supported set: " + str(supported_types)
        )
        return _type
    elif isinstance(path, str) and path:
        _type = path.split(".")[-1]
        _type = _type.replace("md", "markdown")
        if polars:
            _type = _type.replace("jsonl", "ndjson")
        if _type in supported_types:
            return _type
    return None
