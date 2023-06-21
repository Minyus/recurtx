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

    if package == "pandas":
        import pandas as pd

        kwargs.setdefault("dtype", str)
        kwargs.setdefault("keep_default_na", False)
    elif package == "modin":
        import modin.pandas as pd
    elif package == "polars":
        import polars as pd
    else:
        raise NotImplementedError()
    import numpy as np

    ls = []
    for path in paths:
        df = pd.read_csv(path, **kwargs)
        if query:
            df = df.query(query)
        ls.append(df)

    df = pd.concat(ls)

    if method:
        df = eval("df." + method)
        if not isinstance(df, pd.DataFrame):
            text = "{}".format(df)
            if write_path:
                Path(write_path).write_text(text)
            else:
                print(text)
            return

    if write_path:
        if package == "polars":
            df.write_csv(write_path)
        else:
            df.to_csv(write_path, index=False)
    else:
        if package == "polars":
            print(df.write_csv())
        else:
            print(df.to_csv(index=False))
