<div align="center">

#  Python Super Collections

**Dictionaries as you dreamed them when you were a kid.**

Instantly Convert json and YAML files into objects with attributes.
</div>

```python
import json
from super_collections import SuperDict
with open('my_file.json', 'r') as file:
    data = json.load(file)
document = SuperDict(data)

print(document.author) # instead of document['author'] 
for document in document.blocks: # instead of document['blocks']
    ...
print(document.blocks[3].name) # instead of document['blocks'][3]['name'] -- eek! 🤢

```
________

<!-- To update, run the following command:
markdown-toc -i README.md 
-->

<!-- toc -->

- [Python Super Collections](#python-super-collections)
  - [How it works](#how-it-works)
    - [Superdicts](#superdicts)
    - [Superlists](#superlists)
  - [Install](#install)
    - [From the repository](#from-the-repository)
  - [Usage](#usage)
  - [Restrictions](#restrictions)
  - [Does it work?](#does-it-work)

<!-- tocstop -->

## How it works

There are several packages that quickly convert json or YAML files into 
dictionaries that contain dictionaries, lists etc.

If you want to properly use those data structures in Python, one solution is 
to create dataclasses: [the standard ones](https://docs.python.org/3/library/dataclasses.html), or those of [Pydantic](https://docs.pydantic.dev/latest/concepts/dataclasses/).

But sometimes, it is overkill. You just want your app to quickly load
data and navigate through them.

That's where **superdicts** a **superlists** are handy.

### Superdicts
A **superdict** is simply a dictionary whose keys (at least those that
are valid identifiers) are automatically accessible as attributes.

```python
d = SuperDict({'foo':5, 'bar': 'hello'})

# instead of writing d['foo']
d.foo = 7
```


If a SuperDict contains a value that is itself a dictionary, that
dictionary is converted in turn into a SuperDict.

### Superlists
A **superlist** is a list where all dictionary items have been
(automagically) converted to **superdicts**.

SuperLists, combined with SuperDicts make sure that your most complex
datastructures (from json or YAML) can be recursively converted into 
well-behaved Python  objects.




## Install


### From the repository

```sh
pip install super-collections
```

## Usage

```python
from super_collections import SuperDict, SuperList

d = SuperDict({'foo':5, 'bar': 'hello'})
l = SuperList([5, 7, 'foo', {'foo': 5}])
```

You can cast any dictionary and list into its "Super" equivalent when you want, and you are off to the races. 

**The casting is recursive** i.e. in the case above, you can assert:

```python
l[-1].foo == 5
```

All methods of dict and list are available.


Those objects are self documented. `d.properties()` is a generator
that lists all keys that are available as attributes.

```python
list(d.properties())
> ['foo', 'bar']
dir(d)
> ['__class__', ..., 'bar', 'clear', 'copy', 'foo', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'properties', 'setdefault', 'to_hjson', 'to_json', 'update', 'values']
```

This means the **auto-complete feature** might be available
for the attributes of a SuperDict within a code editor (if the dictionary was
statically declared in the code); or in an advanced REPL
(such as [bpython](https://bpython-interpreter.org/)).

The methods `dict.update(other_dict)` and `list.extend(other_list)` 
automatically cast the contents into SuperDict and SuperList as needed.

## Restrictions

1. In a SuperDict, **only keys that are valid Python identifiers
   can be accessed as attributes**. If 'bar' is a key of object `foo`,
   you can write `foo.bar`; but you can't
   write ~~`foo.hello world`~~ because 'hello world' is not a 
   valid Python identifier; 
   you will have to access that specific value with the "dictionary" notation: 
   `foo['hello world']`.
2. Similarly, you can't use pre-existing methods of the
   `dict` class: `keys`, `items`, `update`, etc. as properties; as well as the
   `properties` method itself (wich is specific to SuperDict).
   In that case again, use the dictionary notation to access
   the value (`d['items']`, etc.). Those keys that
   cannot be accessed as attributes are said to be **masked**.
   If you are uncertain which are available, just use 
3. Updating a single element (`d['foo']` for a SuperDict and `l[5]`
    for a SuperList) does not perfom any casting. That's to avoid crazy
    recursive situations, while giving
    you fine grain control on what you want to do 
    (just cast with `SuperDict()` and `SuperList()`).


## Does it work?

Yes. It is tested with pytest. See the `test` directory for examples.