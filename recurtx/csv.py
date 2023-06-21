import sys
from pathlib import Path


def csv(
    *paths: str,
    package: str = "pandas",
    query: str = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    """CSV file transformation using pandas, modin, or polars package specified by package arg"""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("package", None)
    kwargs.pop("query", None)
    kwargs.pop("method", None)
    kwargs.pop("write_path", None)

    if package == "polars":
        import polars as pl

        ls = []
        for path in paths:
            df = pl.scan_csv(path, **kwargs)
            ls.append(df)

        df = pl.concat(ls)

        if method is not None:
            df = eval("df." + method)
            df = df.collect()
            if not isinstance(df, pl.DataFrame):
                text = "{}".format(df)
                if write_path:
                    Path(write_path).write_text(text)
                else:
                    sys.stdout.write(text)
                return

        df = df.collect()

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
