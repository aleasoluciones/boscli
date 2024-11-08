# Boscli

[![CI](https://github.com/aleasoluciones/boscli/actions/workflows/ci.yml/badge.svg)](https://github.com/aleasoluciones/boscli/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/aleasoluciones/boscli/badge.svg)](https://coveralls.io/github/aleasoluciones/boscli)
![Python versions supported](https://img.shields.io/badge/supports%20python-3.9%20|%203.10%20|%203.11%20|%203.12-blue.svg)
[![License](https://img.shields.io/github/license/aleasoluciones/boscli)](https://github.com/aleasoluciones/boscli/blob/master/LICENSE)

**Boscli** is the base infrastructure to create *ad hoc* shells or command line interfaces using Python.

It includes an engine for command completion, types verification, command help and other useful features. It can be used with readline to provide advanced line editing, history and autocompletion.

## Examples

See [examples](examples) dir for a minimal ad hoc shell using readline.

## Installation

You can install the latest sources from GitHub in your project.

```bash
python -m pip install -e git+git://github.com/aleasoluciones/boscli.git#egg=boscli
```

## Specs

To run the Boscli specs you should create a virtual environment, install the development requirements and then run `mamba`.

```bash
python -m pip install -r requirements-dev.txt
mamba
```

## Contribute

If you'd like to contribute, fork [repository](http://github.com/aleasoluciones/boscli), and send a pull request.
