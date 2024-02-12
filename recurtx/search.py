import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple, Union

from .utils import subprocess_run

from importlib.util import find_spec


def run_search(
    text: str,
    target: Union[str, List, Tuple, Set],
    path: Path,
    sub: Optional[Union[str, List, Tuple, Set]] = None,
    wildcard: str = "*",
    separator: str = "/",
    verbose: int = 1,
    context: Optional[int] = None,
    plain: bool = False,
) -> str:
    assert isinstance(separator, str), str(separator) + ": " + str(type(separator))

    if isinstance(target, (list, set, tuple)):
        targets = target
    else:
        assert isinstance(target, str), str(type(target))
        targets = target.split(separator) if separator else [target]

    if isinstance(sub, (list, tuple, set)):
        subs = sub
    elif sub is None:
        subs = [None] * len(targets)
    else:
        assert isinstance(sub, str), str(type(sub))
        subs = sub.split(separator) if separator else [sub]

    assert len(targets) == len(subs), str(len(targets)) + " != " + str(len(subs))

    for _target, _sub in zip(targets, subs):
        target_ls = eval("'''" + _target + "'''").split(wildcard)

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
                if _sub is not None:
                    replacing = text[start_index:end_index]
                    replacing_ls.append(replacing)
                if verbose >= 1:
                    if context is not None:
                        n_lines = context + 1
                        pre_context = "\n".join(
                            text[0:start_index].rsplit("\n", n_lines)[-n_lines:]
                        )
                        post_context = "\n".join(
                            text[end_index:].split("\n", n_lines)[:n_lines]
                        )
                    else:
                        pre_context = ""
                        post_context = ""
                    title = f">> {path} [{start_index}:{end_index}]"
                    target = text[start_index:end_index]
                    if (not find_spec("rich")) or plain:
                        print(title)
                        print(pre_context, end="")
                        print(target, end="")
                        print(post_context)
                    else:
                        from rich.console import Console

                        rc = Console()

                        rc.print(title)
                        rc.print(pre_context, end="")
                        rc.print(target, style="bold red", end="")
                        rc.print(post_context)
            else:
                break
        for replacing in list(set(replacing_ls)):
            text = text.replace(replacing, _sub)

    return text


def search(
    target: str,
    path: str,
    sub: Optional[str] = None,
    wildcard: str = "*",
    separator: str = "/",
    verbose: int = 1,
    context: Optional[int] = 1,
    plain: bool = False,
) -> None:
    """Search a keyword, which may include wildcards, in the text file content, and optionally substitute (replace)."""
    target = str(target)
    path = str(path)
    sub = str(sub) if sub is not None else sub

    _path = Path(path)
    try:
        text = _path.read_text()
    except Exception:
        if verbose >= 3:
            raise
        return

    text = run_search(
        text=text,
        target=target,
        path=_path,
        sub=sub,
        wildcard=wildcard,
        separator=separator,
        verbose=verbose,
        context=context,
        plain=plain,
    )

    if sub is not None:
        _path.write_text(text)


def find(
    target: str,
    path: str,
    sub: Optional[str] = None,
    wildcard: str = "*",
    separator: str = "/",
    verbose: int = 1,
    plain: bool = False,
) -> None:
    """Find a keyword, which may include wildcards, in the file path, and optionally substitute (replace)."""
    target = str(target)
    path = str(path)
    sub = str(sub) if sub is not None else sub

    text = path
    _path = Path(path)

    text = run_search(
        text=text,
        target=target,
        path=_path,
        sub=sub,
        wildcard=wildcard,
        separator=separator,
        verbose=verbose,
        plain=plain,
    )

    if (sub is not None) and _path.exists() and (text != path):
        sub_path = Path(text)
        sub_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess_run(["mv", str(_path), str(sub_path)], verbose=False)
