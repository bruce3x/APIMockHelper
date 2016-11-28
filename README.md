# APIMockHelper

[![PyPI version](https://badge.fury.io/py/api.mock.svg)](https://pypi.python.org/pypi/api.mock/1.0.4)

Push config files to Android device. See more https://github.com/brucezz/APIMock

## Installation

Install by `pip`:

```
pip install api.mock --upgrade
```

## USAGE

> $ api.mock -h

```
API Mock Helper.

Usage:
    api.mock [init | push] [-d DIR] [-v | --verbose]
    api.mock clean remote [-d DIR] [-v | --verbose]
    api.mock clean local [-v | --verbose]

    api.mock (-h | --help)
    api.mock --version

Options:
    init                Generate default config files.
    push                Push configs to Android device.
    clean remote        Remove config files on Android device.
    clean local         Remove local config files.
    -d DIR              The location of config files (default current directory).
    -v --verbose        Print more messages.
    -h --help           Show this message.
    --version           Show version.

More information see:
  https://github.com/brucezz/APIMockHelper
  https://github.com/brucezz/APIMock


```