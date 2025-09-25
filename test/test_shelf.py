"""
Test the Shelf structure
"""
import pytest
from super_collections.shelf import Shelf, Cell  

# ---------------------
# Simple cases
# ---------------------
def test_append_and_access_by_index():
    """Test that values can be appended and accessed by index and label."""
    s = Shelf()
    s.append("apple")
    s.append("banana", label="fruit")
    assert s[0] == "apple"
    assert s[1] == "banana"
    assert s["fruit"] == "banana"

def test_duplicate_label_raises():
    """Test that appending a duplicate label raises ValueError."""
    s = Shelf()
    s.append("carrot", label="veg")
    with pytest.raises(ValueError):
        s.append("cucumber", label="veg")

def test_get_label_and_index():
    """Test retrieval of label from index and index from label."""
    s = Shelf()
    s.append("stone")
    s.append("leaf", label="plant")
    assert s.get_label(1) == "plant"
    assert s.get_index("plant") == 1

def test_setitem_by_index_and_label():
    """Test value assignment by index and label."""
    s = Shelf()
    s.append("x")
    s.append("y", label="thing")
    s[0] = "X"
    s["thing"] = "Y"
    assert s[0] == "X"
    assert s["thing"] == "Y"

def test_set_new():
    """Test value assignment (new) by label."""
    s = Shelf()
    s["thing"] = "Y"
    assert s["thing"] == "Y"
    print("Set:", s)
    s["foo"] = "Z"
    s["foo"] = "A"
    assert len(s) == 2
    assert s["foo"] == 'A'

def test_delitem_by_index_and_label():
    """Test deletion of cells by index and label, and cardfile cleanup."""
    s = Shelf()
    s.append("a")
    s.append("b", label="bee")
    del s[0]
    assert len(s) == 1
    assert "bee" in s
    del s["bee"]
    assert len(s) == 0
    assert "bee" not in s

def test_pop_variants():
    """Test pop behavior with no key, index, label, and fallback default."""
    s = Shelf()
    s.append("one")
    s.append("two", label="second")
    assert s.pop() == "two"
    assert s.pop(0) == "one"
    s.append("three", label="third")
    assert s.pop("third") == "three"
    assert s.pop("missing", default="fallback") == "fallback"

def test_get_with_default():
    """Test safe retrieval with fallback default."""
    s = Shelf()
    s.append("x", label="ex")
    assert s.get("ex") == "x"
    assert s.get("why", default="Z") == "Z"

def test_keys_values_items():
    """Test dict-like access to keys, values, and items."""
    s = Shelf()
    s.append("a")
    s.append("b", label="bee")
    s.append("c", label="sea")
    assert set(s.keys()) == {0, "bee", "sea"}
    assert list(s.values()) == ["a", "b", "c"]
    assert dict(s.items()) == {0: "a", "bee": "b", "sea": "c"}

def test_rename_label():
    """Test relabeling of a cell and cardfile update."""
    s = Shelf()
    s.append("x", label="old")
    s.rename("old", "new")
    assert "new" in s
    assert "old" not in s
    assert s["new"] == "x"

def test_update_existing_and_new():
    """Test bulk update of existing and new labeled cells."""
    s = Shelf()
    s.append("a", label="alpha")
    s.update({"alpha": "A", "beta": "B"})
    assert s["alpha"] == "A"
    assert s["beta"] == "B"

def test_contains_behavior():
    """Test membership checks for index and label."""
    s = Shelf()
    s.append("x")
    s.append("y", label="yes")
    assert 0 in s
    assert "yes" in s
    assert "no" not in s
    assert 2 not in s

# ---------------------
# Constructors
# ---------------------

def test_init_with_list():
    """Test Shelf initialized with a single list of values."""
    s = Shelf(["a", "b", "c"])
    assert len(s) == 3
    assert s[0] == "a"
    assert s[1] == "b"
    assert s[2] == "c"
    assert list(s.keys()) == [0, 1, 2]

def test_init_with_dict():
    """Test Shelf initialized with a single dict of labeled values."""
    s = Shelf({"x": 1, "y": 2})
    assert len(s) == 2
    assert s["x"] == 1
    assert s["y"] == 2
    assert set(s.keys()) == {"x", "y"}

def test_init_with_args_and_kwargs():
    """Test Shelf initialized with mixed unlabeled and labeled values."""
    s = Shelf("a", "b", x="c", y="d")
    assert len(s) == 4
    assert s[0] == "a"
    assert s[1] == "b"
    assert s["x"] == "c"
    assert s["y"] == "d"
    assert list(s) == ['a', 'b', 'c', 'd']
    assert list(s.keys()) == [0, 1, "x", "y"]

def test_init_with_list_and_args():
    """Test Shelf initialized with a list and additional positional values."""
    s = Shelf(["a", "b"], "c")
    assert len(s) == 2
    assert s[0] == ["a", "b"]
    assert s[1] == "c"
    assert list(s.keys()) == [0, 1]

def test_init_with_dict_and_kwargs():
    """Test Shelf initialized with a dict and additional labeled values."""
    s = Shelf({"x": 1}, y=2)
    assert len(s) == 2
    assert s["x"] == 1
    assert s["y"] == 2
    assert list(s) == [1, 2]
    assert list(s.keys()) == ["x", "y"]

def test_from_list_constructor():
    """Test Shelf.from_list creates unlabeled cells from a list."""
    s = Shelf.from_list(["apple", "banana"])
    assert len(s) == 2
    assert s[0] == "apple"
    assert s[1] == "banana"
    assert list(s.keys()) == [0, 1]

def test_from_dict_constructor():
    """Test Shelf.from_dict creates labeled cells from a dict."""
    s = Shelf.from_dict({"fruit": "apple", "veg": "carrot"})
    assert len(s) == 2
    assert s["fruit"] == "apple"
    assert s["veg"] == "carrot"
    assert list(s) == ['apple', 'carrot']
    assert list(s.keys()) == ["fruit", "veg"]

def test_init_with_invalid_type():
    """Test Shelf initialization with unsupported type raises TypeError."""
    with pytest.raises(TypeError):
        Shelf(42)

def test_init_with_duplicate_labels():
    """Test Shelf initialization with duplicate labels raises ValueError."""
    with pytest.raises(ValueError):
        Shelf({"x": 1}, x=2)

def test_from_dict_with_duplicate_labels():
    """Test Shelf.from_dict with duplicate keys is allowed (dict keys are unique)."""
    s = Shelf.from_dict({"x": 1, "y": 2})
    assert s["x"] == 1
    assert s["y"] == 2

def test_from_list_with_non_list_raises():
    """Test Shelf.from_list with non-list input raises TypeError."""
    with pytest.raises(TypeError):
        Shelf.from_list("not a list")

def test_from_dict_with_non_dict_raises():
    """Test Shelf.from_dict with non-dict input raises TypeError."""
    with pytest.raises(TypeError):
        Shelf.from_dict(["not", "a", "dict"])
