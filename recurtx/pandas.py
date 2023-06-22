import sys
from pathlib import Path


def pandas(
    *paths: str,
    package: str = "pandas",
    query: str = None,
    head: int = None,
    tail: int = None,
    sample: int = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    """file transformation using pandas package"""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("package", None)
    kwargs.pop("query", None)
    kwargs.pop("head", None)
    kwargs.pop("tail", None)
    kwargs.pop("sample", None)
    kwargs.pop("method", None)
    kwargs.pop("write_path", None)

    if package == "modin":
        import modin.pandas as pd
    elif package == "pandas":
        import pandas as pd
    else:
        raise NotImplementedError(
            "'" + package + "' not supported. Set one of ['pandas', 'modin']"
        )
    import numpy as np

    kwargs.setdefault("dtype", str)
    kwargs.setdefault("keep_default_na", False)

    ls = []
    for path in paths:
        df = pd.read_csv(path, **kwargs)
        if query:
            df = df.query(query)
        ls.append(df)

    df = pd.concat(ls, ignore_index=True)

    subset_ls = []
    if head is not None:
        subset_ls.append(df.head(head))
    if tail is not None:
        subset_ls.append(df.tail(tail))
    if subset_ls:
        df = pd.concat(subset_ls, ignore_index=True)

    if sample is not None:
        df = df.sample(sample)

    if method is not None:
        df = eval("df." + method)
        if not isinstance(df, pd.DataFrame):
            text = "{}".format(df)
            if write_path:
                Path(write_path).write_text(text)
            else:
                sys.stdout.write(text)
            return

    if write_path:
        df.to_csv(write_path, index=False)
    else:
        sys.stdout.write(df.to_csv(index=False))
