"""
Testing Super Collections with their json serial output.

Several issues have be raised with serialization problem
and we need a way to really test different cases.


(C) Laurent Franceschetti 2025
"""

from datetime import datetime, date





from super_collections import SuperDict, SuperList

CITIES = 'Geneva', 'Lausanne', 'Bern', 'Zurich', 'Sankt-Gallen' 

MIX1 = 'Foo', 1, datetime(2025, 9, 11, 14, 59), None, {'foo': 5, 'bar': 6}, date(2025, 9, 11)

MIX2 = {'Foo': 2, 'Bar': MIX1, 'Baz': CITIES}


def test_simple():
    """
    Test a simple super-collection
    """

    tree = SuperList(CITIES)
    print(tree.to_hjson())


def test_mix():
    """
    Test mixed super-collection
    """

    tree = SuperList(MIX1)
    print(tree.to_hjson())