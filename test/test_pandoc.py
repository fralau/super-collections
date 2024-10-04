"""
Testing Super Collections with a pandoc-generated file
(https://pandoc.org)

The purpose is to show a practical application.

It could be done directly on lists and dictionary, but it would
be awkward. The code is much more legible and maintainable.


(C) Laurent Franceschetti 2024
"""

import os
import json

import pytest


from super_collections import SuperDict, SuperList

# -------------------------------------
# Constants
# -------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PANDOC_FILE = 'test_pandoc.json'


# -------------------------------------
# Code
# -------------------------------------

def strip_format(sl: SuperList) -> str:
    "Print pandoc text from a super list"
    if not isinstance(sl, SuperList):
        raise ValueError(f"{sl} not a list")
    r = []
    for element in sl:
        if isinstance(element, (str, int)):
            pass
        elif isinstance(element, list):
            r.append(strip_format(element))
        elif element.t == 'Str':
            r.append(element.c)
        elif element.t == 'Space':
            r.append(' ')
        elif isinstance(element.c, list):
            r.append(strip_format(element.c))
    return ''.join(r)

def test_read_json_file():
    """
    Read the JSON file using the function and convert it into a SuperDict
    """
    filename = os.path.join(CURRENT_DIR, PANDOC_FILE)
    with open(filename, 'r') as file:
        data = json.load(file)
    document = SuperDict(data)

    print('\n----')
    lines = []
    for block in document.blocks:
        # change the header level
        if block.t == 'Header':
            block.c[0] += 1
        lines.append(strip_format(block.c))
    result = '\n'.join(lines)
    print(result)
    assert "fairly heavy" in result
    assert "Title level 2" in result



