Simple BST and AVL-Tree impl. Requires Python3.8 (cause of `:=` walrus operator)

Caveats:
- no comparability check (no Pythonic way of doing this) of data you insert, so don't expect correct work with `dict`s, `set`s and other objects which implement `__gt__`,`__lt__`, but are not obviously comparable. Also, no check for `None`, so you can create `Node` with `Node.value==None`, but expect `TypeError` when trying to instert that to a non-empty tree.

Installation:
`python3 setup.py install`
