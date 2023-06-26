import sys
from pathlib import Path


def run_search(
    text: str,
    target: str,
    path: Path,
    sub: str = None,
    wildcard: str = "*",
    separator: str = "/",
    verbose: int = 1,
):
    assert isinstance(separator, str), str(separator) + ": " + str(type(separator))

    if isinstance(target, (list, tuple, set, dict)):
        targets = target
    else:
        assert isinstance(target, str), str(type(target))
        if separator:
            targets = target.split(separator)
        else:
            targets = [target]

    if isinstance(sub, (list, tuple, set, dict)):
        subs = sub
    elif sub is None:
        subs = [None] * len(targets)
    else:
        assert isinstance(sub, str), str(type(sub))
        if separator:
            subs = sub.split(separator)
        else:
            subs = [sub]

    assert len(targets) == len(subs), str(len(targets)) + " != " + str(len(subs))

    for target, sub in zip(targets, subs):
        target_ls = eval("'''" + target + "'''").split(wildcard)

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
        for replacing in list(set(replacing_ls)):
            text = text.replace(replacing, sub)

    return text


def search(
    target: str,
    path: str,
    sub: str = None,
    wildcard: str = "*",
    separator: str = "/",
    verbose: int = 1,
):
    """Search a keyword, which may include wildcards, in the text file content, and optionally substitute (replace)."""

    path = Path(path)
    try:
        text = path.read_text()
    except Exception:
        if verbose >= 3:
            raise
        return

    text = run_search(
        text=text,
        target=target,
        path=path,
        sub=sub,
        wildcard=wildcard,
        separator=separator,
        verbose=verbose,
    )

    if sub is not None:
        path.write_text(text)


def find(
    target: str,
    path: str,
    sub: str = None,
    wildcard: str = "*",
    separator: str = "/",
    verbose: int = 1,
):
    """Find a keyword, which may include wildcards, in the file path, and optionally substitute (replace)."""

    text = path
    path = Path(path)

    text = run_search(
        text=text,
        target=target,
        path=path,
        sub=sub,
        wildcard=wildcard,
        separator=separator,
        verbose=verbose,
    )

    if sub is not None:
        path.rename(text)
