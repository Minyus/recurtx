import sys
from pathlib import Path


def activate(
    df,
    fetch: int = None,
    streaming: bool = None,
):
    df = (
        df.fetch(n_rows=fetch, streaming=streaming)
        if fetch
        else df.collect(streaming=streaming)
    )
    return df


def csv(
    *paths: str,
    package: str = "pandas",
    streaming: str = None,  # actually bool
    fetch: int = None,
    query: str = None,
    head: int = None,
    tail: int = None,
    sample: int = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    """CSV file transformation using pandas, modin, or polars package specified by package arg"""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("package", None)
    kwargs.pop("streaming", None)
    kwargs.pop("fetch", None)
    kwargs.pop("query", None)
    kwargs.pop("head", None)
    kwargs.pop("tail", None)
    kwargs.pop("sample", None)
    kwargs.pop("method", None)
    kwargs.pop("write_path", None)

    streaming = streaming in {"", "True", "true", "T", "t", "1"}

    if package == "polars":
        import polars as pl

        ls = []
        for path in paths:
            df = pl.scan_csv(path, **kwargs)
            ls.append(df)

        df = pl.concat(ls)

        subset_ls = []
        if head is not None:
            subset_ls.append(df.head(head))
        if tail is not None:
            subset_ls.append(df.tail(tail))
        if subset_ls:
            df = pl.concat(subset_ls)

        if sample is not None:
            df = activate(df, fetch, streaming)
            df = df.sample(sample)
            df = df.lazy()

        if method is not None:
            df = eval("df." + method)
            df = activate(df, fetch, streaming)
            if not isinstance(df, pl.DataFrame):
                text = "{}".format(df)
                if write_path:
                    Path(write_path).write_text(text)
                else:
                    sys.stdout.write(text)
                return

        df = activate(df, fetch, streaming)

        if write_path:
            df.write_csv(write_path)
        else:
            sys.stdout.write(df.write_csv())
        return

    if package == "modin":
        import modin.pandas as pd
    elif package == "pandas":
        import pandas as pd
    else:
        raise NotImplementedError(
            "'" + package + "' not supported. Set one of ['pandas', 'modin', 'polars']"
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
