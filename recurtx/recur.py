import sys
from pathlib import Path

from .utils import get_exception_msg, subprocess_run, upath


def recur(
    kind: str,
    path: str,
    *scripts: str,
    **kwargs: str,
):
    glob = kwargs.pop("glob", "**/*")
    reverse = kwargs.pop("reverse", False)
    replace_str = kwargs.pop("replace_str", "@@")
    show_paths = kwargs.pop("show_paths", False)
    show_scripts = kwargs.pop("show_scripts", False)

    scripts = list(scripts)
    if len(kwargs) and len(scripts) == 1:
        scripts = scripts[0].split(" ")
    for k, v in kwargs.items():
        if isinstance(v, bool) and v == False:
            continue
        if len(k) >= 2:
            scripts.append("--" + k)
        elif len(k) == 1:
            scripts.append("-" + k)
        else:
            raise NotImplementedError()
        if isinstance(v, bool):
            continue
        scripts.append(str(v))

    if not scripts:
        scripts = ["echo"]

    if replace_str and all([replace_str not in script for script in scripts]):
        if len(scripts) >= 2:
            scripts.append(replace_str)
        else:
            scripts[0] += " " + replace_str

    path = Path(upath(path))
    assert path.exists(), str(path.resolve()) + " does not exist."

    if path.is_file():
        path_ls = [str(path)]
    else:
        path_ls = [str(p) for p in path.glob(glob) if p.is_file()]
        path_ls.sort(reverse=reverse)
    if show_paths:
        sys.stdout.write(
            "[Searching files]\n" + str("\n".join(["    " + p for p in path_ls]) + "\n")
        )

    running_scripts = scripts
    if kind == "under":
        for p in path_ls:
            try:
                if replace_str:
                    running_scripts = [
                        script.replace(replace_str, p) for script in scripts
                    ]
                if len(running_scripts) == 1:
                    running_scripts = running_scripts[0]
                subprocess_run(running_scripts, show_scripts)
            except Exception:
                msg = get_exception_msg()
                sys.stdout.write(msg)
                continue

    elif kind == "batch":
        if len(scripts) == 1:
            running_scripts = scripts[0]
            if replace_str:
                running_scripts = running_scripts.replace(
                    replace_str, " ".join(path_ls)
                )
        else:
            running_scripts = []
            for script in scripts:
                if replace_str and (script == replace_str):
                    running_scripts.extend(path_ls)
                else:
                    running_scripts.append(script)
        try:
            subprocess_run(running_scripts, show_scripts)
        except Exception:
            msg = get_exception_msg()
            sys.stdout.write(msg)
    else:
        raise NotImplementedError()


def under(
    path: str,
    *scripts: str,
    **kwargs: str,
):
    """Run any scripts for each file under a directory recursively."""

    kind = "under"
    recur(
        kind,
        path,
        *scripts,
        **kwargs,
    )


def batch(
    path: str,
    *scripts: str,
    **kwargs: str,
):
    """Run any scripts for a batch of files in a directory recursively."""

    kind = "batch"
    recur(
        kind,
        path,
        *scripts,
        **kwargs,
    )
