# recurtx

[![Python version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://pypi.org/project/recurtx/)
[![PyPI version](https://badge.fury.io/py/recurtx.svg)](https://badge.fury.io/py/recurtx)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Minyus/recurtx/blob/main/LICENSE)

CLI to transform text files recursively

## Commands

### recurtx under

Run any command for each file under a directory recursively.

#### Example

Run `wc -l {FILEPATH}` for each file under `directory_foo` recursively:

```
recurtx under directory_foo "wc -l"
```

#### recurtx under --help

```
NAME
    recurtx under

SYNOPSIS
    recurtx under PATH <flags> [SCRIPTS]...

POSITIONAL ARGUMENTS
    PATH
        Type: str
    SCRIPTS
        Type: str

FLAGS
    -g, --glob=GLOB
        Type: str
        Default: '**/*'
    -r, --replace_str=REPLACE_STR
        Type: str
        Default: '@@'
    -a, --append_missing_replace_str=APPEND_MISSING_REPLACE_STR
        Type: bool
        Default: True
    -v, --verbose=VERBOSE
        Type: int
        Default: 1

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

### recurtx search

Search a keyword in a file.

#### Example

Search `keyword_bar` in each file under `directory_foo` recursively:

```
recurtx under directory_foo recurtx search keyword_bar
```

#### recurtx search --help

```
NAME
    recurtx search

SYNOPSIS
    recurtx search TARGET PATH <flags>

POSITIONAL ARGUMENTS
    TARGET
        Type: str
    PATH
        Type: str

FLAGS
    -s, --sub=SUB
        Type: Optional[str]
        Default: None
    -w, --wildcard=WILDCARD
        Type: str
        Default: '*'
    -v, --verbose=VERBOSE
        Type: int
        Default: 1

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

## Dependencies

- https://github.com/google/python-fire
