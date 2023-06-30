from pathlib import Path
from typing import List, Optional

from .utils import infer_type, stdout_lines

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

TRUE_VALUES = {"", "True", "true", "T", "t", "1"}


def activate(
    df,
    fetch: Optional[int] = None,
    streaming: Optional[bool] = None,
):
    return (
        df.fetch(n_rows=fetch, streaming=streaming)
        if fetch
        else df.collect(streaming=streaming)
    )


def polars(
    *paths: str,
    read_type: Optional[str] = None,
    columns: Optional[List[str]] = None,
    excluding_columns: Optional[List[str]] = None,
    filepath_column: Optional[str] = None,
    streaming: Optional[str] = None,  # actually bool
    fetch: Optional[int] = None,
    join: Optional[str] = None,
    on: Optional[str] = None,
    left_on: Optional[str] = None,
    right_on: Optional[str] = None,
    suffix: str = "_right",
    validate: str = "m:m",
    head: Optional[int] = None,
    tail: Optional[int] = None,
    sample: Optional[int] = None,
    method: Optional[str] = None,
    write_type: Optional[str] = None,
    write_path: Optional[str] = None,
    **kwargs,
):
    """Read and transform tabular files using polars."""

    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("read_type", None)
    kwargs.pop("columns", None)
    kwargs.pop("excluding_columns", None)
    kwargs.pop("filepath_column", None)
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
    kwargs.pop("write_type", None)
    kwargs.pop("write_path", None)

    _write_type = (
        infer_type(write_type, write_path, DATA_TYPES.union({"markdown"}), polars=True)
        or "csv"
    )

    streaming_flag = streaming in TRUE_VALUES

    import polars as pl

    ls = []
    for path in paths:
        _read_type = infer_type(read_type, path, DATA_TYPES, polars=True)
        if not _read_type:
            continue

        _kwargs = kwargs.copy()
        if read_type == "csv":
            _kwargs.setdefault("missing_utf8_is_empty_string", True)
            _kwargs.setdefault("infer_schema_length", 0)

        read_func = getattr(pl, "scan_" + _read_type, None)
        if read_func is None:
            read_func = getattr(pl, "read_" + _read_type)
            df = read_func(path, **_kwargs).lazy()
        else:
            df = read_func(path, **_kwargs)

        if columns:
            df = df.select(columns)
        if excluding_columns:
            if isinstance(excluding_columns, str):
                excluding_columns = [excluding_columns]
            _columns = df.columns
            _columns = [c for c in _columns if c not in excluding_columns]
            df = df.select(_columns)

        if filepath_column:
            df = df.with_columns(pl.lit(path).alias(filepath_column))

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
        df = activate(df, fetch, streaming_flag)
        df = df.sample(sample)
        df = df.lazy()

    if method is not None:
        df = eval("df." + method)

    df = activate(df, fetch, streaming_flag)

    if not isinstance(df, pl.DataFrame):
        text = f"{df}"
        if write_path:
            Path(write_path).write_text(text)
        else:
            stdout_lines(text)
        return

    if _write_type == "markdown":

        def write_func(write_path: Optional[str] = None):
            from io import StringIO

            import pandas as pd

            nonlocal df
            csv_text = df.write_csv()
            df = pd.read_csv(StringIO(csv_text), dtype=str, keep_default_na=False)
            return df.to_markdown(write_path, index=False)

    else:
        write_func = getattr(df, "write_" + _write_type)

    if write_path:
        write_func(write_path)
    else:
        text = write_func()
        stdout_lines(text)
