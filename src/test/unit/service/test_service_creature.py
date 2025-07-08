import pytest
from model.creature import Creature
from error import Missing
from service import creature as code

sample = Creature(name="Yeti",
                  country="CN",
                  area="Himalayas",
                  description="Hirsute Himalayan",
                  aka="Abominable Snowman",
                  )

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Yeti")
    assert resp == sample

# Does not work, as is expecting None, while function raises Missing error
# def test_get_missing():
#     resp = code.get_one("boxturtle")
#     assert resp is None
    
def test_get_missing():
    with pytest.raises(Missing):
        _ = code.get_one("boxturtle")

