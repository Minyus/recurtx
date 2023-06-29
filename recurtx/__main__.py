import fire

from .pandas import pandas
from .polars import polars
from .recur import batch, under
from .search import find, search
from .stat import stat


def main():
    fire.Fire(
        dict(
            batch=batch,
            pandas=pandas,
            polars=polars,
            find=find,
            search=search,
            stat=stat,
            under=under,
        )
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


def xstat():
    fire.Fire(stat)


if __name__ == "__main__":
    main()
    xpandas()
    xpolars()
    xbatch()
    xunder()
    xfind()
    xsearch()
    xstat()
