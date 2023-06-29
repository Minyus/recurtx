import os
import sys
from collections import Counter
from pathlib import Path

from .utils import upath


def ll(
    *paths: str,
    depth: int = 1,
    glob: str = None,
    type: str = None,
    file_glob: str = "**/*",
    number_limit: int = 1000,
    sort_paths: str = "asc",
    extension_most_common: int = 1,
):
    """Compute statistics for the directory recursively."""

    paths = paths or ["."]

    if not glob:
        assert depth, depth
        glob = "".join(["*/"] * (depth - 1)) + "*"

    stat_ls = []

    for path in paths:
        path = Path(upath(path))

        if type:
            dir_path_ls = [p for p in (path.glob(glob)) if getattr(p, "is_" + type)()]
        else:
            dir_path_ls = list(path.glob(glob))

        if sort_paths:
            assert isinstance(sort_paths, str), sort_paths
            dir_path_ls.sort(reverse=(sort_paths.lower().startswith("desc")))

        for dir_path in dir_path_ls:
            d = _get_stat(
                dir_path=dir_path,
                glob=file_glob,
                type=type,
                number_limit=number_limit,
                extension_most_common=extension_most_common,
            )
            if d:
                stat_ls.append(d)

    _output_stat(stat_ls)


def _get_stat(
    dir_path,
    glob,
    type,
    number_limit,
    extension_most_common,
):
    if dir_path.is_dir():
        path_ls = [p for p in dir_path.glob(glob) if p.is_file()]
    else:
        path_ls = [dir_path]

    if not path_ls:
        return None

    if number_limit:
        path_ls = path_ls[:number_limit]

    if True:
        if True:
            num_files = len(path_ls)

            divisor = 1
            if num_files > number_limit:
                divisor = num_files / number_limit

            path_ls = path_ls[:number_limit]

            size_ls = []
            # mtime_ls = []
            ext_ls = []
            for p in path_ls:
                st = os.stat(p)
                size_ls.append(st.st_size)
                # mtime_ls.append(st.st_mtime)

                ext = p.suffix
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

            total_size *= divisor

            d = dict(path=str(dir_path) + (os.sep if dir_path.is_dir() else ""))

            num_files = "{:,}".format(num_files)
            total_size = "{:,}".format(total_size)
            max_size = "{:,}".format(max_size)

            if type == "file":
                d.update(dict(size=total_size))
            else:
                d.update(
                    dict(
                        num_files=num_files,
                        total_size=total_size,
                        max_size=max_size,
                        # latest_mtime=latest_mtime,
                    )
                )
                d.update(common_ext_dict)

            return d


def _output_stat(stat_ls):
    if True:
        try:
            import pandas as pd

            colalign_ls = None
            if stat_ls:
                colalign_ls = ["right"] * len(stat_ls[0])
                colalign_ls[0] = "left"

            df = pd.DataFrame(stat_ls)
            md = df.to_markdown(index=False, colalign=colalign_ls)
            sys.stdout.write(str(md) + "\n")
        except:
            import json

            sys.stdout.write(json.dumps(stat_ls, indent=2) + "\n")
