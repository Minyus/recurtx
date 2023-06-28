import os
import re
import sys
from collections import Counter
from pathlib import Path

from .utils import get_exception_msg, subprocess_run, upath


def recur(
    path: str,
    *scripts: str,
    **kwargs: str,
):
    glob = kwargs.pop("glob", "**/*")
    regex = kwargs.pop(
        "regex",
        r"^(?!.*(\.git\/|__pycache__\/|\.ipynb_checkpoints\/|\.pytest_cache\/|\.vscode\/|\.idea\/|\.DS_Store)).*$",
    )
    type = kwargs.pop("type", "file")
    sort_paths = kwargs.pop("sort_paths", "asc")
    replace_str = kwargs.pop("replace_str", "@@")
    show_paths = kwargs.pop("show_paths", False)
    show_scripts = kwargs.pop("show_scripts", False)

    if regex:
        rx = re.compile(regex)
    else:
        rx = None

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
        path_ls = [str(p) for p in path.glob(glob) if getattr(p, "is_" + type)()]
        if rx:
            path_ls = [p for p in path_ls if rx.match(p)]
        if sort_paths:
            assert isinstance(sort_paths, str), sort_paths
            path_ls.sort(reverse=(sort_paths.lower().startswith("desc")))

    if show_paths:
        sys.stdout.write(
            "[Searching files]\n" + str("\n".join(["    " + p for p in path_ls]) + "\n")
        )
    return path_ls, scripts, replace_str, show_scripts


def under(
    path: str,
    *scripts: str,
    **kwargs: str,
):
    """Run any scripts for each file under a directory recursively."""

    path_ls, scripts, replace_str, show_scripts = recur(
        path,
        *scripts,
        **kwargs,
    )

    running_scripts = scripts
    for p in path_ls:
        try:
            if replace_str:
                running_scripts = [
                    script.replace(replace_str, p)
                    if isinstance(script, str)
                    else script
                    for script in scripts
                ]
            if len(running_scripts) == 1:
                running_scripts = running_scripts[0]
            subprocess_run(running_scripts, show_scripts)
        except Exception:
            msg = get_exception_msg()
            sys.stdout.write(msg)
            continue


def batch(
    path: str,
    *scripts: str,
    **kwargs: str,
):
    """Run any scripts for a batch of files in a directory recursively."""

    path_ls, scripts, replace_str, show_scripts = recur(
        path,
        *scripts,
        **kwargs,
    )

    running_scripts = scripts
    if len(scripts) == 1:
        running_scripts = scripts[0]
        if replace_str:
            running_scripts = running_scripts.replace(replace_str, " ".join(path_ls))
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


def stat(
    *paths: str,
    number_limit: int = 100,
    extension_most_common: int = 1,
    **kwargs: str,
):
    """Compute statistics for the directory recursively."""

    for path in paths:
        out_ls = []

        dir_path_ls, scripts, replace_str, show_scripts = recur(
            path,
            **kwargs,
        )

        type = kwargs.get("type", "file")

        for dir_path in dir_path_ls:
            path_ls, scripts, replace_str, show_scripts = recur(
                dir_path,
            )

            num_files = len(path_ls)

            divisor = None
            if num_files > number_limit:
                divisor = num_files // number_limit
                path_ls = path_ls[0:num_files:divisor]

            size_ls = []
            # mtime_ls = []
            ext_ls = []
            for p in path_ls:
                st = os.stat(p)
                size_ls.append(st.st_size)
                # mtime_ls.append(st.st_mtime)

                ext = p.split(".")[-1]
                ext_ls.append(ext)

            total_size = sum(size_ls)
            max_size = max(size_ls)
            # latest_mtime = max(mtime_ls)
            if extension_most_common:
                common_ext_count_ls = Counter(ext_ls).most_common(extension_most_common)
                common_ext_dict = {
                    "ext_" + str(i + 1): common_ext_count_ls[i][0]
                    for i in range(extension_most_common)
                }

            if divisor is not None:
                total_size *= divisor

            d = dict(path=dir_path)
            colalign_ls = ["left"]

            num_files = "{:,}".format(num_files)
            total_size = "{:,}".format(total_size)
            max_size = "{:,}".format(max_size)

            if type == "dir":
                d.update(
                    dict(
                        num_files=num_files,
                        total_size=total_size,
                        max_size=max_size,
                        # latest_mtime=latest_mtime,
                    )
                )
                d.update(common_ext_dict)
                colalign_ls.extend(["right"] * 4)
            else:
                d.update(dict(size=total_size))
                colalign_ls.extend(["right"])

            out_ls.append(d)

        try:
            import pandas as pd

            df = pd.DataFrame(out_ls)
            md = df.to_markdown(index=False, colalign=colalign_ls)
            sys.stdout.write(str(md) + "\n")
        except:
            import json

            sys.stdout.write(json.dumps(out_ls, index=2), "\n")
