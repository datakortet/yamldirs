# -*- coding: utf-8 -*-

"""Test that all modules are importable.
"""

import yamldirs
import yamldirs.filemaker
import yamldirs.yamldirs_cmd


def test_import_():
    "Test that all modules are importable."
    
    assert yamldirs
    assert yamldirs.filemaker
    assert yamldirs.yamldirs_cmd
