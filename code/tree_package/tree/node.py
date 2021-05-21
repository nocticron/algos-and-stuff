from typing import Any
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
    balance = 0

class RBNode(Node):
    """
    Лист красно-чёрного дерева
    """
    colour = None
