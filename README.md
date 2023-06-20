# recurtx

[![Python version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://pypi.org/project/recurtx/)
[![PyPI version](https://badge.fury.io/py/recurtx.svg)](https://badge.fury.io/py/recurtx)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Minyus/recurtx/blob/main/LICENSE)

CLI to transform text files recursively

## Install

### [Option 1] Install from the PyPI

Caveat: an old version could be installed.

```
pip install recurtx
```

### [Option 2] Install with editable option

This is recommended if you want to use the latest version and/or modify the source code.

```bash
git clone https://github.com/Minyus/recurtx.git
cd recurtx
pip install -e .
```

## Commands

### recurtx under

Run any command for each file under a directory recursively.

#### Examples

Run `wc -l {FILEPATH}` for each file under `directory_foo` recursively:

```
recurtx under directory_foo "wc -l"
```

Quoting for the script can be omitted for most cases. 

```
recurtx under directory_foo wc -l
```

Caveat: int, float, tuple, list, dict could be formatted unexpectedly (by `fire` package), for example:
- ` 00 ` (recognized as int by Python) will be converted to ` 0 ` while ` "00" ` (recognized as str by Python) will be kept as is

#### Description

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
    --glob=GLOB
        Type: str
        Default: '**/*'
    --replace_str=REPLACE_STR
        Type: str
        Default: '@@'
    --append_missing_replace_str=APPEND_MISSING_REPLACE_STR
        Type: bool
        Default: True
    --show_paths=SHOW_PATHS
        Type: bool
        Default: False
    --show_scripts=SHOW_SCRIPTS
        Type: bool
        Default: False

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

### recurtx search

Search a keyword in a file.

#### Examples

Search `keyword_bar` in each file under `directory_foo` recursively:

```
recurtx under directory_foo recurtx search keyword_bar
```

Search `keyword_bar` and substitute (replace) with `keyword_baz` in each file under `directory_foo` recursively:

```
recurtx under directory_foo recurtx search keyword_bar --sub keyword_baz
```

#### Description

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
