
.. image:: https://coveralls.io/repos/datakortet/yamldirs/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/datakortet/yamldirs?branch=master


yamldirs
========

Create directories and files (including content) from yaml spec.


This module was created to rapidly create, and clean up, directory trees
for testing purposes.

Installation::

    pip install yamldirs

Usage
-----

The most common usage scenario for testing will typically look like this::

    from yamldirs import create_files

    def test_relative_imports():
        files = """
            foodir:
                - __init__.py
                - a.py: |
                    from . import b
                - b.py: |
                    from . import c
                - c.py
        """
        with create_files(files) as workdir:
            # workdir is now created inside the os's temp folder, containing
            # 4 files, of which two are empty and two contain import
            # statements.

        # `workdir` is automatically removed after the with statement.


If you don't want the workdir to disappear (typically the case if a test fails
and you want to inspect the directory tree) you'll need to change the
with-statement to::

    with create_files(files, cleanup=False) as workdir:
        ...


``yamldirs`` can of course be used outside of testing scenarios too::

    from yamldirs import Filemaker

    Filemaker('path/to/parent/directory', """
        - foo.txt |
            hello
        - bar.txt |
            world
    """)

Syntax
------
The yaml syntax to create a single file::

    foo.txt

a single file containing the text `hello world`::

    foo.txt: |
        hello world

creating two (empty) files::

    - foo.txt
    - bar.txt

two files with content::

    - foo.txt |
        hello
    - bar.txt |
        world

directory with two (empty) files::

    foo:
        - bar
        - baz

empty directory (must be the literal string ``empty``::

    foo:
        - empty


nested directories with files::

    foo:
        - a.txt: |
            contents of the file named a.txt
        - bar:
            - b.txt: |
                contents of the file named b.txt

Extending yamldirs
------------------
To extend ``yamldirs`` to work with other storage backends, you'll need to
inherit from ``yamldirs.filemaker.FilemakerBase`` and override the following
methods::

    class Filemaker(FilemakerBase):
        def goto_directory(self, dirname):
            os.chdir(dirname)

        def makedir(self, dirname, content):
            cwd = os.getcwd()
            os.mkdir(dirname)
            os.chdir(dirname)
            self.make_list(content)
            os.chdir(cwd)

        def make_file(self, filename, content):
            with open(filename, 'w') as fp:
                fp.write(content)

        def make_empty_file(self, fname):
            open(fname, 'w').close()

