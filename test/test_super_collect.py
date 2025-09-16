import pytest
from collections import deque, UserList
from collections.abc import Sequence
from rich import print

from super_collections import SuperList, SuperDict, SuperCollection, super_collect


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
    assert_type({'a': 1}, SuperDict)


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
