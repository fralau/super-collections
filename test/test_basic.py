import os
import json


import pytest


from super_collections import SuperDict, SuperList

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SOLAR_SYSTEM = 'solar_system.json'


def test_dict():
    """
    Test Superdict
    """
    DATA = """{
        "name": "Mercury",
        "size": 4880,
        "mass": 3.30e23,
        "orbit": 57900000,
        "orbit_from": "Sun",
        "length_of_year": 88,
        "moons": [],
        "foo bar": 50,
        "items": "foobar"
      }"""
    
    mercury = json.loads(DATA)
    mercury = SuperDict(mercury)

    # normal diction
    assert 'name' in mercury
    assert 'size' in mercury

    # attributes
    assert mercury.name == 'Mercury'
    assert mercury.size == 4880
    assert mercury.orbit_from == "Sun"

    # discrovery
    assert 'name' in mercury.properties()
    assert 'name' in dir(mercury)
    assert 'orbit_from' in dir(mercury)

    # invalid identifier
    invalid_id = 'foo bar'
    assert invalid_id in mercury
    assert invalid_id not in dir(mercury)
    assert mercury[invalid_id] == 50 # but reachable as a dict key

    # not a valid property (is masked by the standard method `items()`)
    assert mercury['items'] == 'foobar'
    assert 'items' not in mercury.properties()
    assert mercury.items != 'foobar'
    assert callable(mercury.items)
    assert ('size', 4880) in mercury.items()
 



def test_update_list():
    "Update super lists"

    l = SuperList(({'foo': 5, 'bar': 5}, 'baz'))
    assert l[0].foo == 5

    l2 = [6, {'barbaz': 45}]
    l.extend(l2)

    last = l[-1]
    assert last.barbaz == 45


    l3 = ["hello", {'foobar': 30}]

    # add a list to a SuperList -> Superlist
    r1 = l + l3
    assert isinstance(r1, SuperList)
    last = r1[-1]
    assert last.foobar == 30 # this is a SuperDict

    # CAUTION: add a SuperList to a List -> list
    r2 = l3 + l
    assert not isinstance(r2, SuperList)
    with pytest.raises(AttributeError):
        second = r2[1]
        second.foobar # this is NOT a SuperDict


def test_read_json_file():
    """
    Read the JSON file using the function and convert it into a SuperDict
    """
    filename = os.path.join(CURRENT_DIR, SOLAR_SYSTEM)
    with open(filename, 'r') as file:
        data = json.load(file)
    solar_system = SuperDict(data)

    # attributes are recursively available, including with lists:
    units = solar_system.units
    assert units.size == 'km'
    for planet in solar_system.planets:
        assert isinstance(planet, SuperDict)
        print (planet.name, planet.size)
        for moon in planet.moons:
            print(f"- {moon.name}", moon.size)

    ADDITIONAL = [{'name': 'Foo', 'size': 45895},
                  {'name': 'Bar', 'size': 59383}]
    new_planet_list = solar_system.planets + ADDITIONAL
    assert isinstance(new_planet_list, SuperList)
    last_planet = new_planet_list[-1]
    assert last_planet.name == 'Bar'
    assert last_planet.size == 59383
    with pytest.raises(AttributeError):
        last_planet.orbit
    last_planet.orbit = 5930590
    assert last_planet.orbit == 5930590 

if __name__ == "__main__":
    pytest.main()
