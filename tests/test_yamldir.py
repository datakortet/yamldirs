# -*- coding: utf-8 -*-
import os

from yamldirs import create_files


def tree(root):
    def _tree():
        for rt, dirs, files in os.walk(root):
            for name in files:
                yield os.path.join(rt, name)
    return list(sorted(_tree()))


def test_create_file():
    fdef = """
        foo.txt
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]


def test_create_file_content():
    fdef = """
        foo.txt: |
            hello world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]
        assert open(os.path.join(workdir, 'foo.txt')).read() == 'hello world\n'


def test_create_files():
    fdef = """
        - foo.txt
        - bar.txt
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [
            os.path.join(workdir, 'bar.txt'),
            os.path.join(workdir, 'foo.txt')
        ]


def test_create_directory():
    fdef = """
        bar:
            - foo.txt
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [os.path.join(workdir, 'bar', 'foo.txt')]


def test_empty_directory():
    fdef = """
        bar:
            - empty
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        bardir = os.path.join(workdir, 'bar')
        assert os.path.isdir(bardir)
        assert os.listdir(bardir) == []


def test_nested_directory():
    fdef = """
        foo:
            - a
            - bar:
                - b
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        foodir = os.path.join(workdir, 'foo')
        bardir = os.path.join(workdir, 'foo', 'bar')
        assert os.path.isdir(foodir)
        assert os.path.isdir(bardir)
        assert os.listdir(foodir) == ['a', 'bar']
        assert os.listdir(bardir) == ['b']
