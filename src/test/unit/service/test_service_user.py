import pytest
from model.user import User
from error import Missing
from service import user as code

sample = User(name="Homer Simpson",
              hash="abcd",
              )

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Homer Simpson")
    assert resp == sample

# Does not work, as is expecting None, while function raises Missing error
# def test_get_missing():
#     resp = code.get_one("Flying Duck")
#     assert resp is None

def test_get_missing():
    with pytest.raises(Missing):
        _ = code.get_one("Flying Duck")
        

