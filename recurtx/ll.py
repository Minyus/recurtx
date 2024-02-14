import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

from .utils import to_glob, upath


def ll(
    *paths: str,
    depth: int = 1,
    unit_glob: str = "**/*",
    type: Optional[str] = None,
    glob: str = "**/*",
    regex: str = r"^(?!.*(\.git\/|__pycache__\/|\.ipynb_checkpoints\/|\.pytest_cache\/|\.vscode\/|\.idea\/|\.DS_Store)).*$",
    number_limit: int = 100,
    sort_paths: str = "asc",
    info: bool = False,
    extension_most_common: int = 1,
) -> None:
    """Compute statistics for the directory recursively."""

    paths = paths or (".",)

    unit_glob = to_glob(depth) or unit_glob

    stat_ls = []

    for path in paths:
        _path = Path(upath(path))

        if type:
            dir_path_ls = [
                p for p in (_path.glob(unit_glob)) if getattr(p, "is_" + type)()
            ]
        else:
            dir_path_ls = list(_path.glob(unit_glob))

        if sort_paths:
            assert isinstance(sort_paths, str), sort_paths
            dir_path_ls.sort(reverse=(sort_paths.lower().startswith("desc")))

        if info:
            for dir_path in dir_path_ls:
                d = _get_stat(
                    dir_path=dir_path,
                    glob=glob,
                    regex=regex,
                    type=type,
                    number_limit=number_limit,
                    extension_most_common=extension_most_common,
                )
                if d:
                    stat_ls.append(d)
        else:
            sys.stdout.write("\n".join([str(p) for p in dir_path_ls]) + "\n")

    if info:
        _output_stat(stat_ls)


def _get_stat(
    dir_path: Path,
    glob: str,
    regex: Optional[str],
    type: Optional[str],
    number_limit: int,
    extension_most_common: int,
) -> Optional[Dict]:
    rx = re.compile(regex) if regex else None
    if dir_path.is_dir():
        try:
            path_ls = [p for p in dir_path.glob(glob) if p.is_file()]
        except PermissionError:
            return None
    else:
        path_ls = [dir_path]

    if rx:
        path_ls = [p for p in path_ls if rx.match(str(p))]

    if not path_ls:
        return None

    num_files = len(path_ls)

    divisor = None
    if num_files > number_limit:
        divisor = num_files / number_limit

    path_ls = path_ls[:number_limit]

    size_ls = []
    # mtime_ls = []
    ext_ls = []
    for p in path_ls:
        try:
            st = p.stat()
        except Exception:
            continue
        size_ls.append(st.st_size)
        # mtime_ls.append(st.st_mtime)

        ext = p.suffix
        ext_ls.append(ext)

    total_size = sum(size_ls)
    max_size = max(size_ls)
    # latest_mtime = max(mtime_ls)

    common_ext_dict = {}
    if extension_most_common:
        common_ext_count_ls = Counter(ext_ls).most_common(extension_most_common)
        common_ext_dict = {
            "ext_" + str(i + 1): common_ext_count_ls[i][0]
            for i in range(extension_most_common)
        }

    d = {"path": str(dir_path) + (os.sep if dir_path.is_dir() else "")}

    _num_files = f"{num_files:,}"

    if divisor:
        total_size = round(total_size * divisor)
        _total_size = f"~ {total_size:,}"
        _max_size = f">= {max_size:,}"
    else:
        _total_size = f"{total_size:,}"
        _max_size = f"{max_size:,}"

    if type == "file":
        d.update({"size": _total_size})
    else:
        d.update(
            {
                "files": _num_files,
                "total_size": _total_size,
                "max_size": _max_size,
                # "latest_mtime": latest_mtime,
            },
        )
        d.update(common_ext_dict)

    return d


def _output_stat(stat_ls: List[Dict[str, Any]]) -> None:
    try:
        import pandas as pd

        colalign_ls = None
        if stat_ls:
            colalign_ls = ["right"] * len(stat_ls[0])
            colalign_ls[0] = "left"

        df = pd.DataFrame(stat_ls)
        md = df.to_markdown(index=False, colalign=colalign_ls)
        sys.stdout.write(str(md) + "\n")
    except Exception:
        import json

        sys.stdout.write(json.dumps(stat_ls, indent=2) + "\n")
