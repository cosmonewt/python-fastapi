import os
import pytest
from model.explorer import Explorer
from error import Missing, Duplicate

# set this before data imports below for data.init 

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer

@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Claude Hande", country="FE", description="Scarce during full moons")

def test_create(sample):
    resp = explorer.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = explorer.create(sample)

def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        _ = explorer.get_one("Beau Buffalo")

def test_modify(sample):
    explorer.country = "AF"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample

def test_modify_missing():
    person: Explorer = Explorer(name="Beau Buffalo", country="US", description="")
    with pytest.raises(Missing):
        _ = explorer.modify(person.name, person)

def test_delete(sample):
    resp = explorer.delete(sample.name)
    return resp

def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.delete(sample.name)