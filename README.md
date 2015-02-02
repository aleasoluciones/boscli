# Boscli
[![Build status](https://secure.travis-ci.org/aleasoluciones/boscli.svg?branch=master)](https://secure.travis-ci.org/aleasoluciones/boscli)
[![Coverage Status](https://img.shields.io/coveralls/aleasoluciones/boscli.svg)](https://coveralls.io/r/aleasoluciones/boscli?branch=master)

**Boscli** is the base infrastructure to create *ad hoc*
shells or command line interfaces using Python. It includes an useless shell with a minimum set of commands. This shell can be extended using plugins that will be loaded during its own startup.

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
