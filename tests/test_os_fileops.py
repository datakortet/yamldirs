import os
import tempfile
from contextlib import contextmanager


def test_cd_to_tempdir():
    """Test basic temp dir functionality.
    """
    initial_cwd = os.getcwd()
    abspath_tmpdir = tempfile.mkdtemp()
    try:
        assert os.path.isabs(abspath_tmpdir)
        os.chdir(abspath_tmpdir)
        curdir = os.getcwd()
        assert initial_cwd != curdir
        assert curdir == abspath_tmpdir
    finally:
        os.chdir(initial_cwd)      # must exit directory..
        os.rmdir(abspath_tmpdir)  # ..before it can be removed


@contextmanager
def tempdir():
    cwd = os.getcwd()
    tmpdir = tempfile.mkdtemp()
    try:
        os.chdir(tmpdir)
        yield tmpdir
    finally:
        os.chdir(cwd)
        os.rmdir(tmpdir)


def test_tempdir_context():
    cwd = os.getcwd()
    with tempdir() as folder:
        assert folder != cwd
        curdir = os.getcwd()
        assert folder == curdir
