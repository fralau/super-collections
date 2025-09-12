"""
Testing Super Collections with their json serial output.

Several issues have be raised with serialization problem
and we need a way to really test different cases.


(C) Laurent Franceschetti 2025
"""

from datetime import datetime, date, time
import json
from collections import UserDict


from rich import print as rprint


from super_collections import SuperDict, SuperList, json_encode

# -------------------------
# Encoder (alone)
# -------------------------

# 1. Date/time objects
def test_datetime_serialization():
    dt = datetime(2023, 5, 17, 15, 30)
    encoded = json_encode(dt)
    assert '"2023-05-17T15:30:00"' in encoded

def test_date_serialization():
    d = date(2023, 5, 17)
    encoded = json_encode(d)
    assert '"2023-05-17"' in encoded

def test_time_serialization():
    t = time(15, 30)
    encoded = json_encode(t)
    assert '"15:30:00"' in encoded

# 2. UserDict conversion
def test_userdict_serialization():
    ud = UserDict({'a': 1, 'b': 2})
    encoded = json_encode(ud)
    assert '"a": 1' in encoded and '"b": 2' in encoded

# 3. Function object
def test_function_serialization():
    def sample_func(x): """Adds one."""; return x + 1
    encoded = json_encode(sample_func)
    assert "Function:" in encoded
    assert "Adds one." in encoded

# 4. Object with __str__ defined
class StrOnly:
    def __str__(self):
        return "I am str"

def test_str_fallback():
    obj = StrOnly()
    encoded = json_encode(obj)
    assert '"I am str"' in encoded

# 5. Object with neither __str__ nor __repr__ working
class BrokenRepr:
    def __repr__(self):
        raise Exception("fail")

def test_repr_fallback():
    obj = BrokenRepr()
    encoded = json_encode(obj)
    assert "<OBJECT BrokenRepr>" in encoded  # extreme fallback

# 6. Object that uses str (which is repr)
class NotSerializable:
    pass

def test_typeerror_fallback():
    obj = NotSerializable()
    encoded = json_encode(obj)
    rprint(encoded)
    assert ".NotSerializable object" in encoded

# -------------------------
# With Super Collections
# -------------------------


CITIES = 'Geneva', 'Lausanne', 'Bern', 'Zurich', 'Sankt-Gallen' 

MIX1 = 'Foo', 1, datetime(2025, 9, 11, 14, 59), None, {'foo': 5, 'bar': 6}, date(2025, 9, 11)

MIX2 = {'Foo': 2, 'Bar': MIX1, 'Baz': CITIES, }


def test_simple():
    """
    Test a simple super-collection
    """

    tree = SuperList(CITIES)
    t = tree.to_json()
    rprint(t)
    assert '"Geneva"' in t
    print(tree.to_hjson())


def test_mix():
    """
    Test mixed super-collection
    """

    tree = SuperList(MIX1)
    t = tree.to_json()
    rprint(t)
    assert '"2025-09-11' in t # startswith
    assert 'null' in t
    print(tree.to_hjson())