# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import os
import textwrap

from yamldirs.yamldirs_cmd import directories2yaml

DIRNAME = os.path.dirname(__file__)


def test_dirs_only():
    os.chdir(DIRNAME)
    print("DIRNAME:", DIRNAME)
    with io.open('directories.tmp', 'w', encoding='ascii') as fp:
        directories2yaml('nested', fp)

    out = io.open('directories.tmp', encoding='ascii').read()
    print("OUT:\n", out)

    option1 = out == textwrap.dedent(u"""\
        nested:
          level2a: {}
          level2b: {}
        """)
    option2 = out == textwrap.dedent(u"""\
        nested:
          level2b: {}
          level2a: {}
        """)
    assert option1 or option2
    os.unlink('directories.tmp')
