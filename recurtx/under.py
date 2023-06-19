from pathlib import Path

from .utils import subprocess_run, upath


def under(
    path: str,
    *scripts: str,
    glob: str = "**/*",
    replace_str: str = "@@",
    append_missing_replace_str: bool = True,
    verbose: int = 1,
):
    scripts = list(scripts)
    if not scripts:
        if verbose >= 2:
            print("scripts was not provided.")
        scripts = ["echo"]

    if append_missing_replace_str and all(
        [replace_str not in script for script in scripts]
    ):
        if len(scripts) >= 2:
            scripts.append(replace_str)
        else:
            scripts[0] += " " + replace_str

    path = Path(upath(path))
    assert path.exists(), path

    if path.is_file():
        path_ls = [path]
    else:
        path_ls = [p for p in path.glob(glob) if p.is_file()]
    if verbose >= 3:
        print(
            "[Searching files]\n" + str("\n".join(["    " + str(p) for p in path_ls]))
        )

    for p in path_ls:
        try:
            running_scripts = [
                script.replace(replace_str, str(p)) for script in scripts
            ]
            if len(running_scripts) == 1:
                running_scripts = running_scripts[0]
            subprocess_run(running_scripts, verbose >= 2)
        except Exception:
            if verbose >= 3:
                raise
            continue
