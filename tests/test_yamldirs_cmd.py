# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import textwrap

from tests.testpkg.foo import foo
from yamldirs import create_files
from yamldirs.yamldirs_cmd import main, directory2yaml, reconstitute_directory

DIRNAME = os.path.dirname(__file__)


def test_foo():
    assert foo() == 42


def test_directory2yaml(capsys):
    os.chdir(DIRNAME)
    directory2yaml('testpkg', sys.stdout)
    std = capsys.readouterr()
    # print("STD:OUT:", std.out)
    assert std.out == textwrap.dedent(u"""\
        testpkg:
          foo.py: |-
            def foo():
                return 42
          __init__.py: ''
          """)


def test_reconstitute_directory():
    fdef = """
        hello: world
    """
    with create_files(fdef, cleanup=True):
        open('foo.yaml', 'w').write(textwrap.dedent(u"""\
               testpkg:
                  foo.py: |-
                    def foo():
                        return 42
                  __init__.py: ''    
          """))
        reconstitute_directory('foo.yaml')
        assert os.path.exists('testpkg/foo.py')
