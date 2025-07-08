import pytest
from model.explorer import Explorer
from error import Missing
from service import explorer as code

sample = Explorer(name="Claude Hande",
                  country="FE",
                  description="Scarce during full moons",
                  )

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Claude Hande")
    assert resp == sample

# Does not work, as is expecting None, while function raises Missing error
# def test_get_missing():
#     resp = code.get_one("Anonymous")
#     assert resp is None

def test_get_missing():
    with pytest.raises(Missing):
        _ = code.get_one("Anonymous")

