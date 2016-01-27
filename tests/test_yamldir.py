# -*- coding: utf-8 -*-
import os
import textwrap
import warnings

import pytest
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


def test_create_file_content2():
    fdef = """
        foo.txt: hello world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]
        assert open(os.path.join(workdir, 'foo.txt')).read() == 'hello world'


def test_create_file_multiline_content():
    fdef = """
        foo.txt: |
            Lorem ipsum dolor sit amet, vis no altera doctus sanctus,
            oratio euismod suscipiantur ne vix, no duo inimicus
            adversarium. Et amet errem vis. Aeterno accusamus sed ei,
            id eos inermis epicurei. Quo enim sonet iudico ea, usu
            et possit euismod.
    """
    lorem = textwrap.dedent("""\
        Lorem ipsum dolor sit amet, vis no altera doctus sanctus,
        oratio euismod suscipiantur ne vix, no duo inimicus
        adversarium. Et amet errem vis. Aeterno accusamus sed ei,
        id eos inermis epicurei. Quo enim sonet iudico ea, usu
        et possit euismod.
        """)
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]
        assert open(os.path.join(workdir, 'foo.txt')).read() == lorem


def test_create_empty_files():
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


def test_create_files():
    fdef = """
        - foo.txt: |
            hello
        - bar.txt: |
            world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [
            os.path.join(workdir, 'bar.txt'),
            os.path.join(workdir, 'foo.txt')
        ]
        assert open(os.path.join(workdir, 'foo.txt')).read() == 'hello\n'
        assert open(os.path.join(workdir, 'bar.txt')).read() == 'world\n'


def test_create_directory():
    fdef = """
        bar:
            - foo.txt
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        assert tree(workdir) == [os.path.join(workdir, 'bar', 'foo.txt')]


def test_empty_directory(recwarn):
    fdef = """
        bar:
            - empty
    """
    warnings.simplefilter('always')  # catch DeprecationWarnings

    with create_files(fdef, cleanup=True) as workdir:
        assert os.listdir('.') == ['bar']
        bardir = os.path.join(workdir, 'bar')
        assert os.path.isdir(bardir)
        os.chdir(bardir)
        assert os.listdir('.') == []

    assert len(recwarn) == 1
    assert recwarn.pop(DeprecationWarning)


def test_empty_directory2():
    fdef = """
        bar: []
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
        assert set(os.listdir(foodir)) == {'a', 'bar'}
        assert os.listdir(bardir) == ['b']


def test_nested_directory_json():
    fdef = """
        {
            "foo": [
                "a",
                "bar": ["b"]
            ]
        }
    """
    with create_files(fdef, cleanup=True) as workdir:
        print "WORKDIR:", workdir
        print tree(workdir)
        foodir = os.path.join(workdir, 'foo')
        bardir = os.path.join(workdir, 'foo', 'bar')
        assert os.path.isdir(foodir)
        assert os.path.isdir(bardir)
        assert set(os.listdir(foodir)) == {'a', 'bar'}
        assert os.listdir(bardir) == ['b']
