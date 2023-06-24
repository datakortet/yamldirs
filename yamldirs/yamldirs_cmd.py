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
    dirs_only = kw.get('dirs_only', False)

    exclude.append('__pycache__')

    def _tree():
        for rt, dirs, files in os.walk(dirname):
            if not kw.get('dot'):
                for dname in [d for d in dirs if d.startswith('.')]:
                    dirs.remove(dname)
            for d in exclude:
                if d in dirs:
                    dirs.remove(d)
            if dirs_only:
                for d in dirs:
                    yield os.path.join(rt, d)
            else:
                for name in files:
                    if name in exclude:
                        continue
                    if name.endswith('~'):
                        continue
                    if name.endswith('.pyc'):
                        continue
                    if not kw.get('dot'):
                        if name.startswith('.'):
                            continue
                    yield os.path.join(rt, name)

    return list(sorted(_tree()))


def directories2yaml(dirname, stream=sys.stdout, **args):
    res = {}
    args.pop('dirs_only', None)

    for d in tree(dirname, dirs_only=True, **args):
        parts = d.replace('\\', '/').split('/')
        # print(d, parts)
        cur = res
        for part in parts:
            cur.setdefault(part, {})
            cur = cur[part]

    yaml = YAML()
    yaml.default_flow_style = False
    yaml.dump(res, stream)


def files2yaml(files):
    res = {}
    for filename in files:
        parts = filename.replace('\\', '/').split('/')
        cur = res
        for part in parts[:-1]:
            cur.setdefault(part, {})
            cur = cur[part]
        txt = ''
        cur[parts[-1]] = txt
    
    yaml = YAML()
    yaml.default_flow_style = False
    stream = io.StringIO()
    yaml.dump(res, stream)
    return stream.getvalue()


def directory2yaml(dirname, stream=sys.stdout, no_text=False, **args):
    res = {}

    for filename in tree(dirname, **args):
        # print("FILENAME:", filename)
        if filename.endswith('.pyc'):
            continue
        parts = filename.replace('\\', '/').split('/')
        cur = res
        for part in parts[:-1]:
            cur.setdefault(part, {})
            cur = cur[part]
        txt = ''
        if not no_text:
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
    p.add_argument('--dirs-only', action='store_true', default=False, help="only store directories, not files.")
    p.add_argument('--no-text', action='store_true', default=False, help="include text of files")

    args = p.parse_args()
    extracting = args.dirname.endswith('.yaml')
    # to_yaml = not extracting

    if args.dirs_only:
        directories2yaml(**dict(args._get_kwargs()))
    elif extracting:
        reconstitute_directory(args.dirname)
    else:
        directory2yaml(**dict(args._get_kwargs()))
