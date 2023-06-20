import fire

from .csv import csv
from .find import find
from .recur import batch, under
from .search import search


def main():
    fire.Fire(
        dict(
            batch=batch,
            csv=csv,
            find=find,
            search=search,
            under=under,
        )
    )


if __name__ == "__main__":
    main()
