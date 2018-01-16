# imports - standard imports
import os.path as osp
import shutil

# imports - third-party imports
import pytest

# imports - module imports
from bench import utils

def test_assign_if_empty():
    assert utils.assign_if_empty('foo', 'bar') == 'foo'
    assert utils.assign_if_empty(None,  'bar') == 'bar'

@pytest.fixture
def tempdir():
    tempdir = osp.join('foo','bar')
    yield tempdir
    shutil.rmtree(tempdir)

def test_makedirs(tempdir):
    utils.makedirs(tempdir)
    assert osp.exists(tempdir) == True

    with pytest.raises(OSError):
        utils.makedirs(tempdir, exist_ok = False)

def test_check_url():
    assert utils.check_url('http://google.com')         == True
    assert utils.check_url('foobar', raise_err = False) == False

    with pytest.raises(TypeError):
        utils.check_url('foobar')