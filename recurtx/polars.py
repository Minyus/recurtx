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
    join: str = None,
    on: str = None,
    left_on: str = None,
    right_on: str = None,
    suffix: str = "_right",
    validate: str = "m:m",
    head: int = None,
    tail: int = None,
    sample: int = None,
    method: str = None,
    write_path: str = None,
    **kwargs,
):
    """Read and transform tabular files using polars."""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("streaming", None)
    kwargs.pop("fetch", None)
    kwargs.pop("join", None)
    kwargs.pop("on", None)
    kwargs.pop("left_on", None)
    kwargs.pop("right_on", None)
    kwargs.pop("suffix", "_right")
    kwargs.pop("validate", "m:m")
    kwargs.pop("head", None)
    kwargs.pop("tail", None)
    kwargs.pop("sample", None)
    kwargs.pop("method", None)
    kwargs.pop("write_path", None)

    streaming = streaming in {"", "True", "true", "T", "t", "1"}

    if read_type is not None:
        assert read_type in DATA_TYPES, (
            str(read_type) + "not in the supported list: " + str(DATA_TYPES)
        )

    import polars as pl

    ls = []
    for path in paths:
        if read_type is None:
            _read_type = path.split(".")[-1].replace("jsonl", "ndjson")
        else:
            _read_type = read_type
        if _read_type not in DATA_TYPES:
            continue
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
    elif join is not None:
        df = ls[0]
        for right_df in ls[1:]:
            df = df.join(
                right_df,
                on=on,
                how=join,
                left_on=left_on,
                right_on=right_on,
                suffix=suffix,
                validate=validate,
            )
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
