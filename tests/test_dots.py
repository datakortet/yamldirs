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
    with io.open('dots.tmp', 'w', encoding='ascii') as fp:
        directory2yaml('dots', fp)
    out = io.open('dots.tmp', encoding='ascii').read()
    print("OUT:\n", out)

    assert out == textwrap.dedent(u"""\
        {}
        """)
    os.unlink('dots.tmp')
