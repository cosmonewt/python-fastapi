import os
import pytest
from model.user import User
from error import Missing, Duplicate

# set this before data imports below for data.init

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import user

@pytest.fixture
def sample () -> User:
    return User(name="Test User", hash="abcde")

def test_create(sample):
    resp = user.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = user.create(sample)

def test_get_one(sample):
    resp = user.get_one(sample.name)
    assert resp == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        _ = user.get_one("Homer Simpson")

def test_modify(sample):
    user.hash = "wxyz"
    resp = user.modify(sample.name, sample)
    assert resp == sample

def test_modify_missing():
    profile: User = User(name="Homer Simpson", hash="efghi")
    with pytest.raises(Missing):
        _ = user.modify(profile.name, profile)

def test_delete(sample):
    resp = user.delete(sample.name)
    return resp

def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = user.delete(sample.name)