"""
Testing Super Collections with YAML.
"""
import yaml

from datetime import datetime, date
from super_collections import SuperDict, SuperList, yaml_support

CITIES = 'Geneva', 'Lausanne', 'Bern', 'Zurich', 'Sankt-Gallen' 
MIX1 = 'Foo', 1, datetime(2025, 9, 11, 14, 59), None, {'foo': 5, 'bar': 6}, date(2025, 9, 11)
MIX2 = {'Foo': 2, 'Bar': MIX1, 'Baz': CITIES, }

yaml_support()

def test_yaml_support_success():
    d = SuperDict({"x": 1})
    l = SuperList(["a", "b"])

    dumped_dict = yaml.dump(d)
    dumped_list = yaml.dump(l)

    assert "x: 1" in dumped_dict
    assert "- a" in dumped_list and "- b" in dumped_list

    d = SuperDict(MIX2)
    dumped_dict = yaml.dump(d)
    print(dumped_dict)

def test_yaml_support_safe_dump():

    yaml_support()

    d = SuperDict({"x": 1})
    dumped = yaml.safe_dump(d)

    assert "x: 1" in dumped
    assert "!SuperDict" not in dumped  # no tagging expected

