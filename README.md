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

## Wrapper Commands

### xunder

Run any scripts for each file under a directory recursively.

#### Examples

Run `wc -l {FILEPATH}` for each file under `directory_foo` recursively:

```
xunder directory_foo "wc -l"
```

Quoting for the script can be omitted for most cases. 

```
xunder directory_foo wc -l
```

Caveat: int, float, tuple, list, dict could be formatted unexpectedly (by `fire` package), for example:
- ` 00 ` (recognized as int by Python) will be converted to ` 0 ` while ` "00" ` (recognized as str by Python) will be kept as is

#### Description

```
NAME
    xunder

SYNOPSIS
    xunder PATH <flags> [SCRIPTS]...

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
    --show_paths=SHOW_PATHS
        Type: bool
        Default: False
    --show_scripts=SHOW_SCRIPTS
        Type: bool
        Default: False

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

### xbatch

Run any scripts for a batch of files in a directory recursively.

#### Examples

Concatenate all the contents in directory_foo.

```
xbatch directory_foo cat
```

#### Description

```
NAME
    xbatch

SYNOPSIS
    xbatch PATH <flags> [SCRIPTS]...

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
    --show_paths=SHOW_PATHS
        Type: bool
        Default: False
    --show_scripts=SHOW_SCRIPTS
        Type: bool
        Default: False

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

## Commands to transform text files

### xsearch

Search a keyword, which may include wildcards, in the text file content, and optionally substitute (replace).

#### Examples

Search `keyword_bar` in each file under `directory_foo` recursively:

```
xunder directory_foo xsearch keyword_bar
```

Search `keyword_bar` and substitute (replace) with `keyword_baz` in each file under `directory_foo` recursively:

```
xunder directory_foo xsearch keyword_bar --sub keyword_baz
```

#### Description

```
NAME
    xsearch

SYNOPSIS
    xsearch TARGET PATH <flags>

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

### xfind

Find a keyword, which may include wildcards, in the file path, and optionally substitute (replace).

#### Examples

Search `keyword_bar` in each file path under `directory_foo` recursively:

```
xunder directory_foo xfind keyword_bar
```

Search `keyword_bar` and substitute (replace) with `keyword_baz` in each file path under `directory_foo` recursively:

```
xunder directory_foo xfind keyword_bar --sub keyword_baz
```

#### Description

```
NAME
    xfind

SYNOPSIS
    xfind TARGET PATH <flags>

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

### xpandas

Read and transform tabular data using pandas.

Regarding options, see the documents for `pandas.read_xxx` such as:
- [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)

Data types supported by pandas (not all were tested):
  - "pickle"
  - "table"
  - "csv"
  - "fwf"
  - "clipboard"
  - "excel"
  - "json"
  - "html"
  - "xml"
  - "hdf"
  - "feather"
  - "parquet"
  - "orc"
  - "sas"
  - "spss"
  - "sql_table"
  - "sql_query"
  - "sql"
  - "gbq"
  - "stata"

#### Install dependency

```
pip install pandas
```

#### Examples

Read files supported by pandas (such as csv and json) under directory_foo and concatenate:

```
xbatch directory_foo xpandas
```

### xpolars

Read and transform tabular data using polars.

Regarding options, see the documents for `polars.scan_xxx` (or `polars.read_xxx` if scan function is not available), such as:
- [polars.scan_csv](https://pola-rs.github.io/polars/py-polars/html/reference/api/polars.scan_csv.html)

Data types supported by polars (not all were tested):
  - "csv"
  - "ipc"
  - "parquet"
  - "database"
  - "json"
  - "ndjson"
  - "avro"
  - "excel"
  - "delta"

#### Install dependency

```
pip install polars
```

#### Examples

Read files supported by polars (such as csv and json) under directory_foo and concatenate:

```
xbatch directory_foo xpolars
```

## Dependency to enable CLI

- https://github.com/google/python-fire
