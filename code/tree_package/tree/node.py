from typing import Any
DEFAULT_HEIGHT = 1 # sets default height for Node without children

class Node:
    """
    Binary tree node.
    Without left<value<right validation!
    """
    value = None
    left = None
    right = None
    def __init__(self, value: Any)-> None:
        self.value = value
    def __repr__(self)->str:
        return str(self.value)

class AVLNode(Node):
    """
    AVL Tree Node
    """
    height = DEFAULT_HEIGHT
    def __repr__(self, with_balance=False) -> str:
        if with_balance:
        # your value could contain ';' already :)
            return str(self.value)+';'+str(self.balance)
        else:
            return str(self.value)
    def recalculate_height(self)->None:
        l = self.left.height if self.left is not None else 0
        r = self.right.height if self.right is not None else 0
        self.height = max(r,l) + DEFAULT_HEIGHT
    @property
    def balance(self)->int:
        l = self.left.height if self.left is not None else 0
        r = self.right.height if self.right is not None else 0
        return r-l

class RBNode(Node):
    """
    Red-black tree node.
    """
    colour = None
