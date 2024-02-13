import subprocess
import sys
import traceback
from pathlib import Path
from time import sleep
from typing import List, Optional, Set, Union


def get_exception_msg() -> str:
    return "".join(traceback.format_exception(*sys.exc_info()))


def upath(
    path: str,
) -> str:
    if isinstance(path, str) and path.startswith("~"):
        path = str(Path.home()) + path[1:]
    if isinstance(path, str) and path.startswith("."):
        path = str(Path.cwd()) + path[1:]
    return path


def subprocess_run(
    script: Union[str, List[str]],
    verbose: bool = True,
) -> subprocess.CompletedProcess:
    if verbose:
        sys.stdout.write(r">>> " + str(script) + "\n")

        sleep(0.2)

    assert script, script
    shell = isinstance(script, str)
    return subprocess.run(script, shell=shell)


def subprocess_run_stdout(
    script: Union[str, List[str]],
    verbose: bool = True,
) -> str:
    if verbose:
        sys.stdout.write(r">>> " + str(script) + "\n")

        sleep(0.2)

    assert script, script
    shell = isinstance(script, str)
    result = subprocess.run(script, shell=shell, stdout=subprocess.PIPE)
    return result.stdout.decode()


def stdout_lines(text: Optional[str]) -> None:
    if not text:
        return None
    if not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)
    return None


def infer_format(
    format: Optional[str],
    path: Optional[str],
    supported_types: Set[str],
    polars: bool = False,
) -> Union[str, None]:
    if isinstance(format, str) and format:
        _format = format
        _format = _format.replace("md", "markdown")
        if polars:
            _format = _format.replace("jsonl", "ndjson")
        assert _format in supported_types, (
            _format + " not in supported set: " + str(supported_types)
        )
        return _format
    if isinstance(path, str) and path:
        _format = path.split(".")[-1]
        _format = _format.replace("md", "markdown")
        if polars:
            _format = _format.replace("jsonl", "ndjson")
        if _format in supported_types:
            return _format
    return None


def to_glob(depth: Optional[int] = None) -> Optional[str]:
    if depth:
        return "".join(["*/"] * (depth - 1)) + "*"
    return None
