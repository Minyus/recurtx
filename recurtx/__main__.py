import fire

from .ll import ll
from .pandas import pandas
from .polars import polars
from .recur import batch, under
from .search import find, search


def main():
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


def xpandas():
    fire.Fire(pandas)


def xpolars():
    fire.Fire(polars)


def xbatch():
    fire.Fire(batch)


def xunder():
    fire.Fire(under)


def xfind():
    fire.Fire(find)


def xsearch():
    fire.Fire(search)


def xll():
    fire.Fire(ll)
