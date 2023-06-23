import sys
from pathlib import Path

DATA_TYPES = {
    "pickle",
    "table",
    "csv",
    "fwf",
    "clipboard",
    "excel",
    "json",
    "html",
    "xml",
    "hdf",
    "feather",
    "parquet",
    "orc",
    "sas",
    "spss",
    "sql_table",
    "sql_query",
    "sql",
    "gbq",
    "stata",
}


def pandas(
    *paths: str,
    package: str = "pandas",
    read_type: str = None,
    join: str = None,
    merge: str = None,
    on: str = None,
    left_on: str = None,
    right_on: str = None,
    left_index: bool = False,
    right_index: bool = False,
    sort: bool = False,
    suffixes: str = ("_x", "_y"),
    copy: bool = True,
    indicator: bool = False,
    validate: str = None,
    lsuffix: str = None,
    rsuffix: str = None,
    query: str = None,
    head: int = None,
    tail: int = None,
    sample: int = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    """Read and transform tabular files using pandas."""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("package", None)
    kwargs.pop("join", None)
    kwargs.pop("merge", None)
    kwargs.pop("on", None)
    kwargs.pop("left_on", None)
    kwargs.pop("right_on", None)
    kwargs.pop("left_index", False)
    kwargs.pop("right_index", False)
    kwargs.pop("sort", False)
    kwargs.pop("suffixes", ("_x", "_y"))
    kwargs.pop("copy", True)
    kwargs.pop("indicator", False)
    kwargs.pop("validate", None)
    kwargs.pop("lsuffix", "")
    kwargs.pop("rsuffix", "")
    kwargs.pop("query", None)
    kwargs.pop("head", None)
    kwargs.pop("tail", None)
    kwargs.pop("sample", None)
    kwargs.pop("method", None)
    kwargs.pop("write_path", None)

    if read_type is not None:
        assert read_type in DATA_TYPES, (
            str(read_type) + "not in the supported list: " + str(DATA_TYPES)
        )

    if package == "modin":
        import modin.pandas as pd
    elif package == "pandas":
        import pandas as pd
    else:
        raise NotImplementedError(
            "'" + package + "' not supported. Set one of ['pandas', 'modin']"
        )
    import numpy as np

    ls = []
    for path in paths:
        if read_type is None:
            _read_type = path.split(".")[-1]
        else:
            _read_type = read_type
        if _read_type not in DATA_TYPES:
            continue
        read_func = getattr(pd, "read_" + _read_type)
        _kwargs = kwargs.copy()
        if read_type == "csv":
            _kwargs.setdefault("dtype", str)
            _kwargs.setdefault("keep_default_na", False)
        df = read_func(path, **_kwargs)
        if query:
            df = df.query(query)
        ls.append(df)

    if not ls:
        return
    elif len(ls) == 1:
        df = ls[0]
    elif merge is not None:
        df = ls[0]
        for right_df in ls[1:]:
            if merge == "anti":
                cols = df.columns
                df = (
                    df.reset_index()
                    .merge(
                        right_df,
                        on=on,
                        how="left",
                        left_on=left_on,
                        right_on=right_on,
                        left_index=left_index,
                        right_index=right_index,
                        sort=sort,
                        suffixes=suffixes,
                        copy=copy,
                        indicator=True,
                        validate=validate,
                    )
                    .set_index("index")
                )
                df = df.query('_merge == "left_only"')[cols]
            else:
                df = (
                    df.reset_index()
                    .merge(
                        right_df,
                        on=on,
                        how=merge,
                        left_on=left_on,
                        right_on=right_on,
                        left_index=left_index,
                        right_index=right_index,
                        sort=sort,
                        suffixes=suffixes,
                        copy=copy,
                        indicator=indicator,
                        validate=validate,
                    )
                    .set_index("index")
                )
    elif join is not None:
        df = ls[0]
        for right_df in ls[1:]:
            df = df.join(
                right_df,
                on=on,
                how=join,
                lsuffix=lsuffix,
                rsuffix=rsuffix,
                sort=sort,
                validate=validate,
            )
    else:
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
