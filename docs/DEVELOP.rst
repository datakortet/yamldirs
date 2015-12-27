

Developing yamldirs
===================


Uploading to PyPI
-----------------

- only source distribution::

    python setup.py sdist upload

- source and windows installer::

    python setup.py sdist bdist_wininst upload

- source, windows, and wheel installer::

    python setup.py sdist bdist_wininst bdist_wheel upload

- create a documentation bundle to upload to PyPi::

    cd build/sphinx/html && zip -r ../../../pypi-docs.zip *


.. note:: if you're using this as a template for new projects, remember to
          `python setup.py register <projectname>` before you upload to
          PyPi.


Running tests
-------------
One of::

    python setup.py test
    py.test yamldirs

with coverage::

    py.test --cov=yamldirs .


Building documentation
----------------------
::

    python setup.py build_sphinx

