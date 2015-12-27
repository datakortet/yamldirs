# -*- coding: utf-8 -*-
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
        self.goto_directory(root)
        self._makefiles(self.fdef)

    def goto_directory(self, dirname):  # pragma: nocover
        """Set current directory to ``dirname``.
           **Must be overridden.**
        """
        print "pushd", dirname

    def makedir(self, dirname, content):  # pragma: nocover
        """Create a new directory named ``dirname``.
           **Must be overridden.** Overriden method must call self.make_list(content).
        """
        print "mkdir " + dirname
        print "pushd " + dirname
        self.make_list(content)
        print "popd"

    def make_file(self, filename, content):  # pragma: nocover
        """Create a new file with name ``filename`` and content ``content``.
           **Must be overridden.**
        """
        print "create file: %s %r" % (filename, content)

    def make_empty_file(self, fname):  # pragma: nocover
        """Create an empty file with filename ``fname``.
           Many backends have special syntax for creating empty files.
           **Must be overridden.**
        """
        print "touch", fname

    def make_list(self, lst):
        """Make a list of items.
        """
        for item in lst:
            self._makefiles(item)

    def _make_empty_file(self, fname):
        # special handling to create empty directories.
        if fname != 'empty':
            self.make_empty_file(fname)

    def _make_file(self, filename, content=None):
        if content is None:
            self._make_empty_file(filename)
        else:
            self.make_file(filename, content)

    def _makefiles(self, f):
        if isinstance(f, dict):
            for k, v in f.items():
                if isinstance(v, list):
                    self.makedir(dirname=k, content=v)
                elif isinstance(v, basestring):
                    self._make_file(filename=k, content=v)
                else:  # pragma: nocover
                    raise ValueError("Unexpected:", k, v)
        elif isinstance(f, basestring):
            self._make_file(f)
        elif isinstance(f, list):
            self.make_list(f)
        else:  # pragma: nocover
            raise ValueError("Unknown type:", f)


class Filemaker(FilemakerBase):
    def goto_directory(self, dirname):
        """Set current directory to ``dirname``.
        """
        os.chdir(dirname)

    def makedir(self, dirname, content):
        """Create a new directory named ``dirname``.
        """
        cwd = os.getcwd()
        os.mkdir(dirname)
        os.chdir(dirname)
        self.make_list(content)
        os.chdir(cwd)

    def make_file(self, filename, content):
        """Create a new file with name ``filename`` and content ``content``.
        """
        with open(filename, 'w') as fp:
            fp.write(content)

    def make_empty_file(self, fname):
        """Create an empty file with filename ``fname``.
        """
        open(fname, 'w').close()


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
        yield tmpdir
    finally:
        os.chdir(cwd)
        if cleanup:  # pragma: nocover
            shutil.rmtree(tmpdir, ignore_errors=True)
