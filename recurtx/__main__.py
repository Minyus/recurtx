import fire

from .find import find
from .pandas import pandas
from .polars import polars
from .recur import batch, under
from .search import search


def main():
    fire.Fire(
        dict(
            batch=batch,
            pandas=pandas,
            polars=polars,
            find=find,
            search=search,
            under=under,
        )
    )


if __name__ == "__main__":
    main()
