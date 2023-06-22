import sys
from pathlib import Path

DATA_TYPES = {
    "csv",
    "ipc",
    "parquet",
    "database",
    "json",
    "ndjson",
    "avro",
    "excel",
    "delta",
}


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


def polars(
    *paths: str,
    read_type: str = None,
    streaming: str = None,  # actually bool
    fetch: int = None,
    head: int = None,
    tail: int = None,
    sample: int = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    """file transformation using polars package"""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("streaming", None)
    kwargs.pop("fetch", None)
    kwargs.pop("head", None)
    kwargs.pop("tail", None)
    kwargs.pop("sample", None)
    kwargs.pop("method", None)
    kwargs.pop("write_path", None)

    streaming = streaming in {"", "True", "true", "T", "t", "1"}

    import polars as pl

    ls = []
    for path in paths:
        if read_type is None:
            _read_type = path.split(".")[-1].replace("jsonl", "ndjson")
            if _read_type not in DATA_TYPES:
                continue
        else:
            assert read_type in DATA_TYPES, (
                read_type + "not in the supported list: " + str(DATA_TYPES)
            )
            _read_type = read_type
        read_func = getattr(pl, "scan_" + _read_type, None)
        if read_func is None:
            read_func = getattr(pl, "read_" + _read_type)
            df = read_func(path, **kwargs).lazy()
        else:
            df = read_func(path, **kwargs)
        ls.append(df)

    if not ls:
        return
    elif len(ls) == 1:
        df = ls[0]
    else:
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

    if write_path:
        df.write_csv(write_path)
    else:
        sys.stdout.write(df.write_csv())
    return
