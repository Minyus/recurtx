from pathlib import Path
from typing import Any, List, Optional, Tuple

from .utils import infer_format, stdout_lines

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
    input_format: Optional[str] = None,
    columns: Optional[List[str]] = None,
    excluding_columns: Optional[List[str]] = None,
    filepath_column: Optional[str] = None,
    join: Optional[str] = None,
    merge: Optional[str] = None,
    on: Optional[str] = None,
    left_on: Optional[str] = None,
    right_on: Optional[str] = None,
    left_index: bool = False,
    right_index: bool = False,
    sort: bool = False,
    suffixes: Tuple[str, str] = ("_x", "_y"),
    copy: bool = True,
    indicator: bool = False,
    validate: Optional[str] = None,
    lsuffix: Optional[str] = None,
    rsuffix: Optional[str] = None,
    query: Optional[str] = None,
    head: Optional[int] = None,
    tail: Optional[int] = None,
    sample: Optional[int] = None,
    method: Optional[str] = None,
    output_format: Optional[str] = None,
    output_path: Optional[str] = None,
    **kwargs: Any,
) -> None:
    """Read and transform tabular files using pandas."""
    """Workaround for unexpected behavior of Fire"""
    kwargs.pop("package", None)
    kwargs.pop("input_format", None)
    kwargs.pop("columns", None)
    kwargs.pop("excluding_columns", None)
    kwargs.pop("filepath_column", None)
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
    kwargs.pop("output_format", None)
    kwargs.pop("output_path", None)

    _output_format = (
        infer_format(output_format, output_path, DATA_TYPES.union({"markdown"}))
        or "csv"
    )

    if package == "modin":
        import modin.pandas as pd
    elif package == "pandas":
        import pandas as pd
    else:
        raise NotImplementedError(
            "'" + package + "' not supported. Set one of ['pandas', 'modin']"
        )
    import numpy as np  # noqa: F401

    if columns and isinstance(columns, str):
        columns = [columns]
    if excluding_columns and isinstance(excluding_columns, str):
        excluding_columns = [excluding_columns]

    ls = []
    for path in paths:
        _input_format = infer_format(input_format, path, DATA_TYPES)
        if not _input_format:
            continue
        read_func = getattr(pd, "read_" + _input_format)
        _kwargs = kwargs.copy()
        if input_format == "csv":
            _kwargs.setdefault("dtype", str)
            _kwargs.setdefault("keep_default_na", False)
            if columns:
                _kwargs.setdefault("usecols", columns)
        df = read_func(path, **_kwargs)

        if columns:
            df = df[columns]
        if excluding_columns:
            _columns = df.columns
            _columns = [c for c in _columns if c not in excluding_columns]
            df = df[_columns]

        if filepath_column:
            df[filepath_column] = path

        if query:
            df = df.query(query)
        ls.append(df)

    if not ls:
        return
    if len(ls) == 1:
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
        text = f"{df}"
        if output_path:
            Path(output_path).write_text(text)
        else:
            stdout_lines(text)
        return

    _write_func = getattr(df, "to_" + _output_format)

    def write_func(
        output_path: Optional[str] = None,
        index: bool = False,
    ) -> Optional[str]:
        nonlocal _write_func, df
        try:
            if _output_format == "json":
                import json

                ls = df.to_dict(orient="records")
                if output_path:
                    with open(output_path, "w") as f:
                        json.dump(ls, f)
                else:
                    return json.dumps(ls)
            return _write_func(output_path, index=index)
        except Exception:
            return _write_func(output_path)

    if output_path:
        write_func(output_path=output_path, index=False)
    else:
        out_text = write_func(output_path=None, index=False)
        stdout_lines(out_text)
