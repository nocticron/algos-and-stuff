from typing import Any
DEFAULT_HEIGHT = 1 # sets default height for Node without children

class Node:
    """
    Лист бинарного дерева
    без валидации left<value<right!
    без проверки value на компарабельность
    (нет pythonic-way это сделать)
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
    Лист АВЛ-дерева
    """
    height = DEFAULT_HEIGHT
    def __repr__(self, with_balance=False) -> str:
        if with_balance:
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
    Лист красно-чёрного дерева
    """
    colour = None

class AVLNodeSmart:
    """
    Лист АВЛ-дерева
    Сам считает высоты себя и передаёт родителю
    """
    def __init__(self, value: Any) -> None:
        self._height = 1
        self._left = None
        self._right = None
        self.value = value
        self.parent = None

    def set_child(self, node, order):
        orders = {1:'_left',2:'_right'}        
        if (other_node:=getattr(self, orders[order-(-1)**(order)])) is not None:
            other_node_height = other_node.height
        else:
            other_node_height = 1
        if node is not None:
            this_node_height = node.height
        else:
            this_node_height = 1
        setattr(self, orders[order], node)
        self._height = max(this_node_height, other_node_height)
        if self.parent is not None:
            self.parent.set_child(self, (int((self.value-self.parent.value)==0))+1)

    @property
    def height(self):
        return self._height
    @property
    def left(self):
        return self._left
    @property
    def right(self):
        return self._right
    @left.setter
    def left(self, node):
        self.set_child(node, 1)
        self.left.parent = self
    @right.setter
    def right(self, node):
        self.set_child(node, 2)
        self.right.parent = self