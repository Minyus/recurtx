from pathlib import Path


def csv(
    *paths: str,
    backend: str = "pandas",
    query: str = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    kwargs.setdefault("dtype", str)
    kwargs.setdefault("keep_default_na", False)

    if backend == "modin":
        import modin.pandas as pd
    elif backend == "pandas":
        import pandas as pd
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
        df.to_csv(write_path, index=False)
    else:
        print(df.to_csv(index=False))
