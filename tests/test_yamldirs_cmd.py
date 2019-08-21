# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import os
import sys
import textwrap

from tests.testpkg.foo import foo
from yamldirs import create_files
from yamldirs.yamldirs_cmd import main, directory2yaml, reconstitute_directory

DIRNAME = os.path.dirname(__file__)


def test_foo():
    assert foo() == 42


def test_directory2yaml():
    os.chdir(DIRNAME)
    print("DIRNAME:", DIRNAME)
    with io.open('foo.tmp', 'w', encoding='ascii') as fp:
        directory2yaml('testpkg', fp)
    out = io.open('foo.tmp', encoding='ascii').read()
    print("OUT:", out)

    option1 = out == textwrap.dedent(u"""\
        testpkg:
          foo.py: |-
            def foo():
                return 42
          __init__.py: ''
          """)
    option2 = out == textwrap.dedent(u"""\
        testpkg:
          __init__.py: ''
          foo.py: |-
            def foo():
                return 42
          """)
    assert option1 or option2


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
