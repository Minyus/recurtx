import re
import sys
from pathlib import Path
from typing import Any, List, Tuple

from .utils import (
    get_exception_msg,
    subprocess_run,
    subprocess_run_stdout,
    to_glob,
    upath,
)


def recur(
    path: str,
    *scripts: str,
    **kwargs: Any,
) -> Tuple[List[str], List[str], str, bool]:
    avoid_fd = kwargs.pop("avoid_fd", None)
    type = kwargs.pop("type", "f")
    depth = kwargs.pop("depth", None)
    glob = kwargs.pop("glob", None)
    absolute_path = kwargs.pop("absolute_path", True)
    regex = kwargs.pop(
        "regex",
        r"^(?!.*(\.git\/|__pycache__\/|\.ipynb_checkpoints\/|\.pytest_cache\/|\.vscode\/|\.idea\/|\.DS_Store)).*$",
    )
    sort_paths = kwargs.pop("sort_paths", "asc")
    replace_str = kwargs.pop("replace_str", "@@")
    show_paths = kwargs.pop("show_paths", False)
    show_scripts = kwargs.pop("show_scripts", False)

    script_ls = list(scripts)
    if len(kwargs) and len(script_ls) == 1:
        script_ls = script_ls[0].split(" ")
    for k, v in kwargs.items():
        if isinstance(v, bool) and not v:
            continue
        if len(k) >= 2:
            script_ls.append("--" + k)
        elif len(k) == 1:
            script_ls.append("-" + k)
        else:
            raise NotImplementedError
        if isinstance(v, bool):
            continue
        script_ls.append(str(v))

    if not script_ls:
        script_ls = ["echo"]

    if replace_str and all(replace_str not in script for script in script_ls):
        if len(script_ls) >= 2:
            script_ls.append(replace_str)
        else:
            script_ls[0] += " " + replace_str

    _path = Path(upath(path))
    assert _path.exists(), str(_path.resolve()) + " does not exist."

    if _path.is_file():
        path_ls = [str(_path)]
    else:
        if avoid_fd:
            path_ls = None
        else:
            path_ls = subprocess_run_stdout(
                "fd "
                + ("" if not type else f"--type {type} ")
                + ("" if depth is None else f"--max-depth {depth} ")
                + ("" if glob is None else f"--glob {glob} ")
                + ("" if not absolute_path else f"--absolute-path ")
                + f"'' {path}",
                verbose=True,
            ).split("\n")
        if not path_ls:
            glob = to_glob(depth) or glob or "**/*"
            path_ls = [
                str(p)
                for p in _path.glob(glob)
                if (not type)
                or getattr(p, "is_" + type.replace("f", "file").replace("d", "dir"))()
            ]
        if regex:
            rx = re.compile(regex)
            path_ls = [p for p in path_ls if rx.match(p)]
        if sort_paths:
            assert isinstance(sort_paths, str), sort_paths
            path_ls.sort(reverse=(sort_paths.lower().startswith("desc")))

    if show_paths:
        sys.stdout.write(
            "[Searching files]" + str("\n".join(["    " + p for p in path_ls]) + "\n")
        )
    return path_ls, script_ls, replace_str, show_scripts


def under(
    path: str,
    *scripts: str,
    **kwargs: str,
) -> None:
    """Run any scripts for each file under a directory recursively."""

    path_ls, script_ls, replace_str, show_scripts = recur(
        path,
        *scripts,
        **kwargs,
    )

    for p in path_ls:
        try:
            running_script_ls = script_ls
            if replace_str:
                running_script_ls = [
                    script.replace(replace_str, p)
                    if isinstance(script, str)
                    else script
                    for script in script_ls
                ]

            if len(running_script_ls) == 1:
                subprocess_run(running_script_ls[0], show_scripts)
            else:
                subprocess_run(running_script_ls, show_scripts)
        except Exception:
            msg = get_exception_msg()
            sys.stdout.write(msg)
            continue


def batch(
    path: str,
    *scripts: str,
    **kwargs: str,
) -> None:
    """Run any scripts for a batch of files in a directory recursively."""

    path_ls, script_ls, replace_str, show_scripts = recur(
        path,
        *scripts,
        **kwargs,
    )

    try:
        if len(script_ls) == 1:
            running_script = script_ls[0]
            if replace_str:
                running_script = running_script.replace(replace_str, " ".join(path_ls))
            subprocess_run(running_script, show_scripts)
        else:
            running_script_ls = []
            for script in script_ls:
                if replace_str and (script == replace_str):
                    running_script_ls.extend(path_ls)
                else:
                    running_script_ls.append(script)

            subprocess_run(running_script_ls, show_scripts)
    except Exception:
        msg = get_exception_msg()
        sys.stdout.write(msg)
