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
    replace_str = kwargs.pop("replace_str", "@@")
    append_missing_replace_str = kwargs.pop("append_missing_replace_str", True)
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

    if append_missing_replace_str and all(
        [replace_str not in script for script in scripts]
    ):
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
    if show_paths:
        sys.stdout.write(
            "[Searching files]\n" + str("\n".join(["    " + p for p in path_ls]))
        )

    if kind == "under":
        for p in path_ls:
            try:
                running_scripts = [script.replace(replace_str, p) for script in scripts]
                if len(running_scripts) == 1:
                    running_scripts = running_scripts[0]
                subprocess_run(running_scripts, show_scripts)
            except Exception:
                msg = get_exception_msg()
                sys.stdout.write(msg)
                continue

    elif kind == "batch":
        if len(scripts) == 1:
            running_scripts = scripts[0].replace(replace_str, " ".join(path_ls))
        else:
            running_scripts = []
            for script in scripts:
                if script == replace_str:
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
    kind = "batch"
    recur(
        kind,
        path,
        *scripts,
        **kwargs,
    )
