# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from .filemaker import Filemaker


def tree(root):
    def _tree():
        for rt, dirs, files in os.walk(root):
            for name in files:
                if name.endswith('~'): continue
                if name.startswith('.'): continue
                yield os.path.join(rt, name)
    return list(sorted(_tree()))


def directory2yaml(dirname):
    res = {}
    for filename in tree(dirname):
        parts = filename.replace('\\', '/').split('/')
        cur = res
        for part in parts[:-1]:
            cur.setdefault(part, {})
            cur = cur[part]
        txt = open(filename).read().replace('\r\n', '\n').strip()
        if txt.count('\n') >= 1:
            txt = LiteralScalarString(txt)
        cur[parts[-1]] = txt
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.dump(res, sys.stdout)


def reconstitute_directory(yamlfile):
    Filemaker(os.getcwd(), open(yamlfile).read())


def main():
    arg = sys.argv[1]
    if arg.endswith('.yaml'):
        reconstitute_directory(arg)
    else:
        directory2yaml(arg)