import sys
from pathlib import Path


def find(
    target: str,
    path: str,
    sub: str = None,
    wildcard: str = "*",
    verbose: int = 1,
):
    """Find a keyword, which may include wildcards, in the file path, and optionally substitute (replace)."""

    target_ls = eval("'''" + target + "'''").split(wildcard)

    text = path

    replacing_ls = []
    end_index = 0

    while True:
        index = end_index
        start_index = None

        for target_ss in target_ls:
            index = text.find(target_ss, index)
            if index >= 0:
                start_index = start_index or index
                index = index + len(target_ss)
            else:
                break
        if start_index and (index >= 0):
            end_index = index
            if sub is not None:
                replacing = text[start_index:end_index]
                replacing_ls.append(replacing)
            if verbose >= 1:
                sys.stdout.write(
                    f"{path} [{start_index}:{end_index}]\n{text[start_index:end_index]}\n"
                )
        else:
            break
    for replacing in replacing_ls:
        text = text.replace(replacing, sub, 1)
    if sub is not None:
        Path(path).rename(text)
