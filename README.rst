Boscli
=======

.. image:: https://secure.travis-ci.org/aleasoluciones/boscli.svg?branch=master
    :target: https://travis-ci.org/aleasoluciones/boscli
    :alt: Build status

.. image:: https://img.shields.io/coveralls/aleasoluciones/boscli.svg
    :target: https://coveralls.io/r/aleasoluciones/boscli?branch=master
    :alt: Coverage Status

**Boscli** is the base infrastructure to create *ad hoc*
shells or command line interfaces using Python. It includes an useless shell with a minimum set of commands. This shell can be extended using plugins that will be loaded during its own startup.

Installation
------------

You can install the latest sources from GitHub.

.. code-block:: bash

     $ pip install -e git+git://github.com/aleasoluciones/boscli.git#egg=boscli

Specs
-----

To run the Boscli specs you should install the development requirements and then run `mamba`.

.. code-block:: bash

    $ pip install -r requirements-dev.txt
    $ mamba

License
-------

Boscli is released under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_.
