# recurtx

[![Python version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://pypi.org/project/recurtx/)
[![PyPI version](https://badge.fury.io/py/recurtx.svg)](https://badge.fury.io/py/recurtx)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Minyus/recurtx/blob/main/LICENSE)

CLI to recursively search and transform text files in xargs style

## Key features

- search and substitute (replace) text in file contents or file paths in place
- installable without sudo (using pip)

## Background

This tool was developed as an opinionated (partial) alternative to the following CLI tools.

- `find` to recursively find file paths
- `fd` to recursively find file paths respecting .gitignore (`fd` is internally used by `xunder` and `xbatch` in default if installed)
- `grep` to search text
- [`rg`](https://github.com/BurntSushi/ripgrep) to search text
- [`ag`](https://github.com/ggreer/the_silver_searcher) to search text
- `sed` to modify text
- `xargs` to repeat similar to for-loop
- `tree` to recursively check file paths
- `du` to check disk usage
- [`csvkit`](https://csvkit.readthedocs.io/en/latest/) to search (and modify) text in csv files
- [`spyql`](https://spyql.readthedocs.io/) to search (and modify) text in csv files
- [`clickhouse-local`](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local)
- [`polars-cli`](https://github.com/pola-rs/polars-cli) to search text in csv files
- [`csvlens`](https://github.com/YS-L/csvlens) to view csv files
- [`rich-cli`](https://github.com/Textualize/rich-cli) to view csv files

This tool is quicker to write although execution might be slower depending on the amount of your text data.

## Install

Prerequisite: Python 3 (3.8 or later recommended)

### [Option 1] Install from PyPI

```
pip install recurtx
```

### [Option 2] Install from source code

This is recommended only if you want to modify the source code.

```bash
git clone https://github.com/Minyus/recurtx.git
cd recurtx
python setup.py develop
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
NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS

NAME
    xsearch - Search a keyword, which may include wildcards, in the text file content, and optionally substitute (replace).

SYNOPSIS
    xsearch TARGET PATH <flags>

DESCRIPTION
    Search a keyword, which may include wildcards, in the text file content, and optionally substitute (replace).

POSITIONAL ARGUMENTS
    TARGET
        Type: str
    PATH
        Type: str

FLAGS
    --sub=SUB
        Type: Optional[typing.Unio...
        Default: None
    -w, --wildcard=WILDCARD
        Type: str
        Default: '*'
    --separator=SEPARATOR
        Type: str
        Default: '/'
    -v, --verbose=VERBOSE
        Type: int
        Default: 1
    -c, --context=CONTEXT
        Type: typing.Union[int, NoneType]
        Default: 1
    -p, --plain=PLAIN
        Type: bool
        Default: False

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

### xll

Alternative to `ls -lah` and `du`.
Show approximate total size and max size in Bytes to respond quickly in default while it takes time to run `du` in a big directory including many files.
Show number of files and the most common file extention(s) as well.

#### Examples

Run under `directory_foo` non-recursively (up to depth 1):

```
xll directory_foo
```

Run under `directory_foo` recursively up to depth 2:

```
xll -d 2 directory_foo
```

#### Description

```
NAME
    xll - Compute statistics for the directory recursively.

SYNOPSIS
    xll <flags> [PATHS]...

DESCRIPTION
    Compute statistics for the directory recursively.

POSITIONAL ARGUMENTS
    PATHS
        Type: str

FLAGS
    -d, --depth=DEPTH
        Type: int
        Default: 1
    -u, --unit_glob=UNIT_GLOB
        Type: str
        Default: '**/*'
    -t, --type=TYPE
        Type: Optional[typing.Unio...
        Default: None
    -g, --glob=GLOB
        Type: str
        Default: '**/*'
    -r, --regex=REGEX
        Type: str
        Default: '^(?!.*(\\.git\\/|__pycache__\\/|\\.ipynb_checkpoints\\/|\\....
    -n, --number_limit=NUMBER_LIMIT
        Type: int
        Default: 100
    -s, --sort_paths=SORT_PATHS
        Type: str
        Default: 'asc'
    -i, --info=INFO
        Type: bool
        Default: True
    -e, --extension_most_common=EXTENSION_MOST_COMMON
        Type: int
        Default: 1
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

- <https://github.com/google/python-fire>
