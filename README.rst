**********
pydanticli
**********

.. image:: https://github.com/codectl/hpctl/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/codectl/hpctl/actions/workflows/ci.yaml
    :alt: CI
.. image:: https://codecov.io/gh/codectl/hpctl/branch/master/graph/badge.svg
    :target: https://app.codecov.io/gh/codectl/hpctl/branch/master
    :alt: codecov
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: code style: black
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: license: MIT

An `argparse <https://docs.python.org/3/library/argparse.html>`__ built on `pydantic <https://docs.pydantic.dev>`__ for
CLI programs.

Tests & linting 🚥
===============
Run tests with ``tox``:

.. code-block:: bash

    # ensure tox is installed
    $ tox

Run linter only:

.. code-block:: bash

    $ tox -e lint

Optionally, run coverage as well with:

.. code-block:: bash

    $ tox -e coverage

License
=======
MIT licensed. See `LICENSE <LICENSE>`__.
