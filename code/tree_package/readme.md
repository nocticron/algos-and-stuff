Simple BST and AVL-Tree impl. Requires Python3.8 (cause of `:=` walrus operator)

Caveats:
- no comparability check (no Pythonic way of doing this) of data you insert, so don't expect correct work with `dict`s, `set`s and other objects which implement `__gt__`,`__lt__`, but are not obviously comparable. Also, no check for `None`, so it is possible to create `Node` with `Node.value==None`, but you should expect `TypeError` when trying to insert that to a non-empty binary tree.

Installation:

`python3 setup.py install`

or

`pip3 install .`

TODO: 
- get rid of `setup.py`
- add some bells and whistles (`flake8`, `balck`, etc.)
- add some tests and benchmarks (and maybe cicd)
- expand this readme with usage examples