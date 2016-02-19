# -*- coding: utf-8 -*-
import textwrap
import warnings
from contextlib import contextmanager
import os
import shutil
import tempfile
import yaml


class FilemakerBase(object):
    """Override marked methods to do something useful.  Base class serves as
       a dry-run step generator.
    """

    def __init__(self, root, fdef):
        self.fdef = yaml.load(fdef)
        self.pushd(root)
        self._make_item(self.fdef)

    def _make_item(self, item):
        if isinstance(item, dict):
            return self.make_dict_item(item)
        elif isinstance(item, basestring):
            return self.make_string_item(item)
        elif isinstance(item, list):
            return self.make_list_item(item)

    def make_string_item(self, s):
        self.make_file(s, "")

    def make_list_item(self, lst):
        for item in lst:
            self._make_item(item)

    def make_dict_item(self, dct):
        for k, v in dct.items():
            if isinstance(v, basestring):
                self.make_file(filename=k, content=v)
            else:
                self.mkdir(k)
                self.pushd(k)
                self._make_item(v)
                self.popd()

    # override the remaining methods.
    def mkdir(self, dirname):  # pragma: nocover
        print "mkdir " + dirname

    def pushd(self, dirname):  # pragma: nocover
        print "pushd " + dirname

    def popd(self):  # pragma: nocover
        print "popd"

    def make_file(self, filename, content):  # pragma: nocover
        """Create a new file with name ``filename`` and content ``content``.
           **Must be overridden.**
        """
        print "create file: %s %r" % (filename, content)


class Filemaker(FilemakerBase):
    def __init__(self, root, fdef):
        self._curdir = []
        super(Filemaker, self).__init__(root, fdef)

    def mkdir(self, dirname):
        os.mkdir(dirname)

    def pushd(self, dirname):
        dirname = os.path.abspath(dirname)
        self._curdir.append(os.getcwd())
        os.chdir(dirname)

    def popd(self):
        os.chdir(self._curdir.pop())

    def make_file(self, filename, content):
        """Create a new file with name ``filename`` and content ``content``.
        """
        with open(filename, 'w') as fp:
            fp.write(content)


@contextmanager
def create_files(filedef, cleanup=True):
    """Contextmanager that creates a directory structure from a yaml
       descripttion.
    """
    cwd = os.getcwd()
    tmpdir = tempfile.mkdtemp()
    try:
        Filemaker(tmpdir, filedef)
        if not cleanup:  # pragma: nocover
            pass
            # print "TMPDIR =", tmpdir
        os.chdir(tmpdir)
        yield tmpdir
    finally:
        os.chdir(cwd)
        if cleanup:  # pragma: nocover
            shutil.rmtree(tmpdir, ignore_errors=True)
