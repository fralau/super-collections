import json
import pytest
from pathlib import Path
from super_collections import SuperCollection, SuperShelf, Cell  




@pytest.fixture
def solar_system():
    path = Path(__file__).parent / "solar_system.json"
    with path.open("r", encoding="utf-8") as f:
        return SuperShelf(json.load(f))

def test_units_are_scalar(solar_system):
    units = solar_system["units"]
    assert isinstance(units, SuperShelf)
    for key in ["size", "mass", "orbit", "length_of_year"]:
        assert isinstance(units[key], str)

def test_planet_count(solar_system):
    planets = solar_system.planets
    assert isinstance(planets, SuperShelf)
    assert len(planets) == 8

def test_moon_access(solar_system):
    earth = next(p for p in solar_system.planets if p.name == "Earth")
    moons = earth.moons
    assert isinstance(moons, SuperShelf)
    assert moons[0]["name"] == "Moon"

def test_moon_access2(solar_system):
    earth = solar_system.planets.find('name', 'Earth')
    moons = earth.moons
    assert isinstance(moons, SuperShelf)
    assert moons[0].name == "Moon"
    assert moons.find('name', 'Moon').orbit_from == earth.name == 'Earth'


def test_nested_structure(solar_system):
    jupiter = solar_system.planets.find('name', 'Jupiter')
    ganymede = jupiter.moons.find('name', 'Ganymede')
    assert ganymede.orbit_from == "Jupiter"
    assert ganymede.mass > 1e23

def test_planetoid_presence(solar_system):
    names = [p["name"] for p in solar_system["planetoids"]]
    assert "Pluto" in names
    assert "Eris" in names
    assert "Ceres" in names

def test_recursive_type_integrity(solar_system):
    def assert_supershelf_structure(obj):
        if isinstance(obj, SuperShelf):
                for el in obj:
                    assert_supershelf_structure(el)
        elif isinstance(obj, Cell):
            pass
        else:
            assert not isinstance(obj, (list, dict)), f"Found raw {type(obj).__name__} outside SuperShelf"

    assert_supershelf_structure(solar_system)


# -------------------------------------
# Property resolution
# -------------------------------------
def assert_property_resolution(obj, name):
    cls = type(obj)
    # 1. Assert property is defined on the class
    assert name in cls.__dict__, f"{name} not found in class __dict__"
    # 2. Assert it's a property descriptor
    assert isinstance(cls.__dict__[name], property), f"{name} is not a property"
    # 3. Assert it resolves without falling into __getattr__
    try:
        value = getattr(obj, name)
    except AttributeError:
        raise AssertionError(f"{name} triggered __getattr__; descriptor resolution failed")
    # 4. Optional: assert value type
    assert isinstance(value, bool), f"{name} did not return a bool (got {type(value)})"

def resolve_attr(obj, name: str):
    cls = type(obj)
    print(f"🔍 Resolving attribute: {name}")
    
    # Step 1: Class-level descriptor
    if name in cls.__dict__:
        attr = cls.__dict__[name]
        print(f"✅ Found in class __dict__: {attr!r}")
        if isinstance(attr, property):
            print("🔧 It's a property descriptor.")
            try:
                val = attr.__get__(obj, cls)
                print(f"📦 Descriptor __get__ returned: {val!r}")
                return val
            except Exception as e:
                print(f"⚠️ Descriptor __get__ raised: {e}")
                return None
        else:
            print("⚠️ Found in class but not a property.")
            return attr

    # Step 2: Instance-level attribute
    if name in obj.__dict__:
        print(f"✅ Found in instance __dict__: {obj.__dict__[name]!r}")
        return obj.__dict__[name]

    # Step 3: Internal key mapping
    if hasattr(obj, 'keys') and name in obj.keys():
        print(f"🔁 Found in internal keys: {obj[name]!r}")
        return obj[name]

    # Step 4: Fallback to getattr
    try:
        val = getattr(obj, name)
        print(f"🧩 getattr fallback returned: {val!r}")
        return val
    except AttributeError as e:
        print(f"❌ getattr fallback failed: {e}")
        return None



def test_properties():
    shelf = SuperShelf('a', 'b')
    assert isinstance(shelf, SuperCollection)
    "Check properties"
    assert '_is_strict_list' in SuperShelf.__dict__, "Property not found in SuperShelf.__dict__"
    assert isinstance(SuperShelf.__dict__['_is_strict_list'], property), "Not a property"
    resolve_attr(shelf, '_is_strict_list')
    resolve_attr(shelf, '_is_strict_dict')
    assert_property_resolution(shelf, '_is_strict_list')
    assert_property_resolution(shelf, '_is_strict_dict')


def test_predicates_list():
    "Test the predicates of a SuperShelf"
    shelf_list = SuperShelf(['a', 'b'])
    assert isinstance(shelf_list, SuperCollection)
    assert shelf_list.is_fully_collected, f"{shelf_list.to_json()} is NOT fully collected"
    print("Shelf list:", shelf_list)
    assert '_is_strict_dict' in type(shelf_list).__dict__, "_is_strict_dict not in class dict"
    print("Type of attribute:", type(getattr(type(shelf_list), '_is_strict_dict', None)))
    assert isinstance(shelf_list, SuperShelf), "not a SuperShelf, can you believe that?"
    assert shelf_list._is_strict_list, "Not a list"


def test_predicates_dict():
    "Test the predicates of a SuperShelf"
    shelf_dict = SuperShelf({'x': 1, 'y': 2})
    assert shelf_dict._is_strict_dict, "Not a dict"


def no_test_supershelf_to_json():
    "Test conversion of SuperShelf to JSON"
    # Strict list shelf: no labels

    shelf_list = SuperShelf(['a', 'b'])
    assert shelf_list.is_fully_collected

    # Strict dict shelf: all labelled
    shelf_dict = SuperShelf({'x': 1, 'y': 2})

    # Hybrid shelf: mixed labels and unlabelled values
    shelf_hybrid = SuperShelf([
        {'earth': 3},
        4,
        {'mars': 5}
    ])

    supershelf = SuperShelf(shelf_list, shelf_dict, shelf_hybrid)
    assert shelf_list.is_fully_collected
    json_string = supershelf.to_json(indent=2)
    print("JSON:", json_string)
    parsed = json.loads(json_string)

    assert parsed == [
        ["a", "b"],
        {"x": 1, "y": 2},
        [{"earth": 3}, 4, {"mars": 5}]
    ]


