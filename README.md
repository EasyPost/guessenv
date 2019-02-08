This is a small program which tries to guess what environment variables will be needed by other Python programs.

[![Build Status](https://travis-ci.com/EasyPost/guessenv.svg?branch=master)](https://travis-ci.com/EasyPost/guessenv)
[![PyPI version](https://badge.fury.io/py/guessenv.svg)](https://badge.fury.io/py/guessenv)

This tool should work on Python 2.7 and Python 3.3+

### Usage

```
guessenv [-h] [-v] [-q] [-O] [-A] [-x EXCLUDE] [-X] files [files ...]
```

By default, guessenv will walk through all the files and directories specified on the command line, look for
patterns which seem to be searching for an environment variable, and print out all of the "required" environment
variables (those accessed through something akin to `os.environ[...]`).

If invoked with the `-O` argument, it will also print out optional environment variables (accessed through
`os.getenv(...)` or `os.environ.get(...)`.

If invoked with the `-A` argument, it will exit non-zero if any "required" environment variables are not currently
present in the environment.

If invoked with the `-v` argument, it will print more verbose information about where variables were found.

If invoked with the `-q` argument, it will print nothing (unless `-A` is also passed and any variables are missing)

The `-x` and `-X` arguments allow you to exclude files or directories when doing recursive searches.

### License

This work is licensed under the ISC license, a copy of which can be found in [LICENSE.txt](LICENSE.txt).
