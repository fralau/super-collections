import os
from collections import deque, UserList
from collections.abc import Sequence
import json

from rich import print
import pytest


from super_collections import SuperList, SuperDict, SuperCollection, super_collect


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

LIST_TYPES = ['CustomListLike']  # Example duck-typed name



class CustomListLike:
    "A custom list, vanilla"
    def __init__(self):
        self._data = [1, 2, 3]

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)
Sequence.register(CustomListLike)


class CustomListLike2:
    "A custom list-like object, of Sequence type"
    def __init__(self):
        pass

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError("Too high")
        value = index * 2
        print("Index, Value:", index, value)
        return value

    def __len__(self):
        return 5
Sequence.register(CustomListLike2)

def assert_type(obj, class_):
    "Syntactic sugar for super_collection test"
    print(f"Testing '{type(obj).__name__}' as {class_}")
    coll_obj = super_collect(obj)
    assert coll_obj is not None, f"Object {type(obj)} translates to None?"
    assert isinstance(coll_obj, class_)
    assert isinstance(coll_obj, SuperCollection)

# ---------------------
# Tests
# ---------------------
def test_super_collect_list():
    obj = super_collect([1, 2])
    print("Obj:", type(obj))
    print("Obj:", type(obj).__name__)
    assert isinstance(obj, SuperList)

def test_super_collect_tuple():
    assert_type((1, 2), SuperList)

def test_super_collect_deque():
    assert_type(deque([1, 2]), SuperList)

def test_super_collect_userlist():
    assert_type(UserList([1, 2]), SuperList)

def test_super_collect_duck_type():
    assert_type(CustomListLike(), SuperList)
    # Registered as sequence:
    assert_type(CustomListLike2(), SuperList)

def test_super_collect_set():
    assert_type({1, 2}, SuperList)

def test_super_collect_dict():
    obj = {'a': 1}
    assert_type(obj, SuperDict)


@pytest.mark.parametrize("bad_type", ["string", b"bytes", bytearray(b"abc")])
def test_super_collect_invalid_types(bad_type):
    with pytest.raises(TypeError):
        print(f"Checking that {bad_type} <{type(bad_type).__name__}> is NOT accepted.")
        super_collect(bad_type)


def test_super_collection_class():
    obj1 = SuperList([1, 3, 5])
    assert isinstance(obj1, SuperCollection)

    obj2 = SuperDict({'a': 5, 'b':7})
    assert isinstance(obj2, SuperCollection)

    obj = SuperCollection.collect([obj1, obj2])
    print("My SuperCollection object:", obj)
    assert isinstance(obj, SuperCollection)


def test_read_json():
    "Test collecting a JSON file into a SuperCollection"
    # This file is actually a dictionary:
    FILENAME = os.path.join(CURRENT_DIR, 'solar_system.json')
    # Open the file and load its contents
    with open(FILENAME, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Now `data` is a Python structure — usually a dict or list
    content = SuperCollection.collect(data)
    print(str(content)[:200])
    print("(...)")
    # Make sure it is reflexive
    content2 = SuperCollection.collect(content)
    assert content == content2
    assert dict(content) == dict(content2)
