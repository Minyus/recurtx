import fire

from .ll import ll
from .pandas import pandas
from .polars import polars
from .recur import batch, under
from .search import find, search


def main() -> None:
    fire.Fire(
        {
            "ll": ll,
            "pandas": pandas,
            "polars": polars,
            "batch": batch,
            "under": under,
            "find": find,
            "search": search,
        },
    )


def xpandas() -> None:
    fire.Fire(pandas)


def xpolars() -> None:
    fire.Fire(polars)


def xbatch() -> None:
    fire.Fire(batch)


def xunder() -> None:
    fire.Fire(under)


def xfind() -> None:
    fire.Fire(find)


def xsearch() -> None:
    fire.Fire(search)


def xll() -> None:
    fire.Fire(ll)
