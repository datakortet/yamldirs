# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import os
import sys
import argparse
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from .filemaker import Filemaker


def tree(dirname, **kw):
    exclude = kw.get('exclude', [])

    def _tree():
        for rt, dirs, files in os.walk(dirname):
            if not kw.get('dot'):
                for dname in [d for d in dirs if d.startswith('.')]:
                    dirs.remove(dname)
            for d in exclude:
                if d in dirs:
                    dirs.remove(d)
            for name in files:
                if name in exclude: 
                    continue
                if name.endswith('~'): 
                    continue
                if not kw.get('dot'):
                    if name.startswith('.'): continue
                yield os.path.join(rt, name)

    return list(sorted(_tree()))


def directory2yaml(dirname, stream=sys.stdout, **args):
    res = {}
    for filename in tree(dirname, **args):
        if filename.endswith('.pyc'):
            continue
        parts = filename.replace('\\', '/').split('/')
        cur = res
        for part in parts[:-1]:
            cur.setdefault(part, {})
            cur = cur[part]
        with io.open(filename) as fp:
            txt = fp.read()
        if txt.count('\n') >= 1:
            txt = LiteralScalarString(txt)
        cur[parts[-1]] = txt

    yaml = YAML()
    yaml.default_flow_style = False
    yaml.dump(res, stream)


def reconstitute_directory(yamlfile):
    Filemaker(os.getcwd(), open(yamlfile).read())


def main():     # pragma: nocover
    p = argparse.ArgumentParser()
    p.add_argument('dirname', help="directory to convert, or filename.yaml to extract")
    p.add_argument('--dot', action='store_true', default=False, help="traverse files/directories starting with .")
    p.add_argument('--exclude', '-x', default=[], nargs="+", metavar="DIRNAME", help="directory to exclude")

    args = p.parse_args()
    extracting = args.dirname.endswith('.yaml')
    # to_yaml = not extracting

    if extracting:
        reconstitute_directory(args.dirname)
    else:
        directory2yaml(**dict(args._get_kwargs()))
