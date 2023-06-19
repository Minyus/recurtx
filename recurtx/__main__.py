import fire

from .search import search
from .under import under


def main():
    fire.Fire(dict(under=under, search=search))


if __name__ == "__main__":
    main()
