# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import os
import sys
import ast
import argparse
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from .filemaker import Filemaker
from .fileattrs import get_mode, get_owner, get_group


class Attrs:
    def __init__(self, user=None, group=None, mode=None):
        self.user = user
        self.group = group
        self.mode = mode

    @classmethod
    def parse(cls, s):
        obj = cls()
        s = s.strip()
        assert s.startswith('attrs(')
        s = s[6:-1]
        attrs = [attr.strip().split('=') for attr in s.split(',')]
        for k, v in attrs:
            k = k.strip()
            if k == 'user':
                obj.user = ast.literal_eval(v.strip())
            if k == 'group':
                obj.group = ast.literal_eval(v.strip())
            if k == 'mode':
                obj.mode = ast.literal_eval(v.strip())
        return obj

    def __bool__(self):
        return bool(self.user or self.group or self.mode)

    def __str__(self):
        if not self: return ""
        res = []
        if self.user:
            res.append('user="%s"' % self.user)
        if self.group:
            res.append('group="%s"' % self.group)
        if self.mode:
            res.append('mode="%s"' % self.mode)
        return "attrs(%s)" % ', '.join(res)


class Node:
    def __init__(self, name):
        self.path = name.replace('\\', '/')
        tmp = self.path.rsplit('/', 1)
        self.name = tmp[-1]
        self.parent = None if len(tmp) == 1 else tmp[0]
        self.attrs = Attrs()

    def fetch_mode(self):
        self.attrs.mode = get_mode(self.path)

    def fetch_owner(self):
        self.attrs.user = get_owner(self.path)

    def fetch_group(self):
        self.attrs.group = get_group(self.path)

    def label(self):
        res = self.name
        if self.attrs:
            res += f' {self.attrs}'
        return res

    def __str__(self):
        return f'{self.__class__.__name__}({self.name} {self.attrs})'

    __repr__ = __str__

    def parts(self):
        return self.path.split('/')

    def __eq__(self, other):
        return self.path == other.path

    def __lt__(self, other):
        return self.path < other.path

    def serialize(self, key, obj):
        pass


class DirNode(Node):
    def __init__(self, name):
        super(DirNode, self).__init__(name)
        self.children = []

    def serialize(self, key, obj):
        children = {}
        for child in self.children:
            child.serialize(child.label(), children)
        obj[key] = children



class FileNode(Node):
    def __init__(self, name):
        super(FileNode, self).__init__(name)
        self.content = None


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
                    yield DirNode(name=os.path.relpath(os.path.join(rt, d), dirname))
            else:
                for name in files:
                    if name in exclude:
                        continue
                    if name.endswith('~'):
                        continue
                    if not kw.get('dot'):
                        if name.startswith('.'):
                            continue
                    yield os.path.join(rt, name)

    return list(sorted(_tree()))



def directories2yaml(dirname, stream=sys.stdout, **args):
    res = {}
    args.pop('dirs_only', None)
    mode = args.pop('mode')
    owner = args.pop('owner')
    group = args.pop('group')

    nodes = {}
    roots = []

    for d in tree(dirname, dirs_only=True, **args):
        if mode: d.fetch_mode()
        if owner: d.fetch_owner()
        if group: d.fetch_group()

        nodes[d.path] = d

    # connect parents/children, detect roots.
    for k, v in nodes.items():
        if v.parent and v.parent in nodes:
            nodes[v.parent].children.append(v)
        else:
            roots.append(v)

    res = {}
    for root in roots:
        root.serialize(key=root.label(), obj=res)

    yaml = YAML()
    yaml.default_flow_style = False
    yaml.dump(res, stream)


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
    p.add_argument('--dirs-only', action='store_true', default=False, help="only store directories, not files.")
    p.add_argument('--mode', action='store_true', help="record/write the file mode")
    p.add_argument('--owner', action='store_true', help="record/write the file owner")
    p.add_argument('--group', action='store_true', help="record/write the file group")

    args = p.parse_args()
    extracting = args.dirname.endswith('.yaml')
    # to_yaml = not extracting

    if args.dirs_only:
        directories2yaml(**dict(args._get_kwargs()))
    elif extracting:
        reconstitute_directory(args.dirname)
    else:
        directory2yaml(**dict(args._get_kwargs()))
