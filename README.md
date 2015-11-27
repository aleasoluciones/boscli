# Boscli
[![Build status](https://secure.travis-ci.org/aleasoluciones/boscli.svg?branch=master)](https://secure.travis-ci.org/aleasoluciones/boscli)
[![Coverage Status](https://img.shields.io/coveralls/aleasoluciones/boscli.svg)](https://coveralls.io/r/aleasoluciones/boscli?branch=master)

**Boscli** is the base infrastructure to create *ad hoc* shells or command line interfaces using Python.
It includes an engine for command completion, types verification, command help and other useful features. It can be used with readline to provide advanced line editing, history and autocompletion.

## use examples
see examples dir for a minimal ad hoc shell using readline.

## Installation
You can install the latest sources from GitHub.
```bash
$ pip install -e git+git://github.com/aleasoluciones/boscli.git#egg=boscli
```
## Specs
To run the Boscli specs you should install the development requirements and then run `mamba`.
```bash
$ pip install -r requirements-dev.txt
$ mamba
```

## License

Boscli is released under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_.

##Contribute

If you'd like to contribute, fork [repository](http://github.com/aleasoluciones/boscli), and send a pull request.
