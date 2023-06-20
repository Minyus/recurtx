import fire

from .search import search
from .under import batch, under


def main():
    fire.Fire(
        dict(
            batch=batch,
            search=search,
            under=under,
        )
    )


if __name__ == "__main__":
    main()
