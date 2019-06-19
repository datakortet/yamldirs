# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import textwrap
import warnings

import pytest
from yamldirs import create_files
from yamldirs.filemaker import UnknownType


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
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]
        assert os.path.isfile('foo.txt')
        assert open('foo.txt').read() == ""


def test_number_filenames():
    fdef = """
        2: "hello"
    """
    with create_files(fdef, cleanup=True) as workdir :
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, '2')]
        assert open(os.path.join(workdir, '2')).read() == 'hello'


def test_date_filenames():
    fdef = """
        2017-10-25: "hello"
    """
    with create_files(fdef, cleanup=True) as workdir :
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, '2017-10-25')]
        assert open(os.path.join(workdir, '2017-10-25')).read() == 'hello'


def test_date_content():
    fdef = """
        foo: 2017-10-25
    """
    with create_files(fdef, cleanup=True) as workdir :
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, 'foo')]
        assert open(os.path.join(workdir, 'foo')).read() == '2017-10-25'


def test_unknown_type():
    fdef = """
        - 2017-10-25T12:54:42.1Z
    """
    with pytest.raises(UnknownType):
        with create_files(fdef, cleanup=True) as workdir :
            pass  # pragma: nocover


def test_number_content():
    fdef = """
        2: 3
    """
    with create_files(fdef, cleanup=True) as workdir :
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, '2')]
        assert open(os.path.join(workdir, '2')).read() == '3'


def test_create_file_content():
    fdef = """
        foo.txt: |
            hello world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]
        assert open(os.path.join(workdir, 'foo.txt')).read() == 'hello world\n'


def test_create_file_content2():
    fdef = """
        foo.txt: hello world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
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
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, 'foo.txt')]
        assert open(os.path.join(workdir, 'foo.txt')).read() == lorem


def test_create_empty_files():
    fdef = """
        - foo.txt
        - bar.txt
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [
            os.path.join(workdir, 'bar.txt'),
            os.path.join(workdir, 'foo.txt')
        ]


def test_create_empty_files2():
    fdef = """
        foo.txt: ""
        bar.txt: ""
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [
            os.path.join(workdir, 'bar.txt'),
            os.path.join(workdir, 'foo.txt')
        ]
        assert open('foo.txt').read() == ""


def test_create_files():
    fdef = """
        - foo.txt: |
            hello
        - bar.txt: |
            world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
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
        print("WORKDIR:", workdir)
        print(tree(workdir))
        assert tree(workdir) == [os.path.join(workdir, 'bar', 'foo.txt')]


def test_mix_empty():
    files = """
        - a.py
        - b:
            - a.txt
            - aa.txt
        - d
        - e:
            - a:
                - b
        - f
    """
    with create_files(files) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
        print("LISTDIR:", os.listdir('.'))
        assert {os.path.relpath(d, workdir) for d in os.listdir('.')} == {
            'a.py', 'b', 'd', 'e', 'f'
        }


def test_empty_directory2():
    fdef = """
        bar: []
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
        bardir = os.path.join(workdir, 'bar')
        assert os.path.isdir(bardir)
        assert os.listdir(bardir) == []


def test_empty_directoryw():
    fdef = """
        bar:
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))
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
        print("WORKDIR:", workdir)
        print(tree(workdir))
        foodir = os.path.join(workdir, 'foo')
        bardir = os.path.join(workdir, 'foo', 'bar')
        assert os.path.isdir(foodir)
        assert os.path.isdir(bardir)
        assert set(os.listdir(foodir)) == {'a', 'bar'}
        assert os.listdir(bardir) == ['b']


def test_nested_directory2():
    fdef = """
        foo:
            bar:
                baz:
                    hello: world
    """
    with create_files(fdef, cleanup=True) as workdir:
        print("WORKDIR:", workdir)
        print(tree(workdir))

        foodir = os.path.join(workdir, 'foo')
        assert os.path.isdir(foodir)

        bardir = os.path.join(workdir, 'foo', 'bar')
        assert os.path.isdir(bardir)
        assert set(os.listdir(foodir)) == {'bar'}

        bazdir = os.path.join(workdir, 'foo', 'bar', 'baz')
        assert os.path.isdir(bazdir)
        assert os.listdir(bazdir) == ['hello']

        hello = os.path.join(bazdir, 'hello')
        assert os.path.isfile(hello)
        assert open(hello).read() == "world"


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
        print("WORKDIR:", workdir)
        print(tree(workdir))
        foodir = os.path.join(workdir, 'foo')
        bardir = os.path.join(workdir, 'foo', 'bar')
        assert os.path.isdir(foodir)
        assert os.path.isdir(bardir)
        assert set(os.listdir(foodir)) == {'a', 'bar'}
        assert os.listdir(bardir) == ['b']
