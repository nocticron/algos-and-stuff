"""
Quick-and-dirty имплементация бинарного дерева поиска
Поддеревья не балансируются
"""
from typing import Iterable, Any, Union, Optional
from .node import Node

class SearchResult:
    """
    Структура для удобста поиска и удаления
    Нужна только тогда, когда нужно передать родителя ноды
    и порядок наследования (left/right)
    """
    def __init__(self, node, parent, order: str)-> None:
        self.node = node
        self.parent = parent
        self.order = order

class NodePoint:
    """
    Обертка листа для печати
    """
    def __init__(self, node, offset: int)-> None:
        self.node = node
        self.offset = offset

class BST:
    """
    Бинарное дерево поиска
    без баланса поддеревьев
    """
    node = Node
    root = None
    printing_offset = 20

    def __init__(self, data: Any, node_type=None):
        if node_type is not None:
            self.node = node_type
        if isinstance(data, Iterable) and data:
            for i in data:
                self.insert(i)
        elif isinstance(data, self.node):
            self.root = data
        else:
            self.root = self.node(data)
        
    def __repr__(self)->str:        
        roots = [NodePoint(self.root, offset=self.printing_offset)]
        def plot_tree(roots, tab=1) -> str:
            """
                Послойная печать дерева
                TODO: выставить вычисляемый отступ у корня
                (сейчас используется заранее выставленнй self.printing_offset)
            """
            q = []
            s = ""
            TAB = " "
            SEP = '\n'
            for root in roots:
                padding = (root.offset - len(s))*TAB
                s = s + padding + str(root.node)
                mid = root.offset + len(str(root.node))//2
                if root.node.left:
                    l = len(str(root.node.left))
                    q.append(NodePoint(root.node.left, mid - l//2 - tab))
                if root.node.right:
                    l = len(str(root.node.right))
                    q.append(NodePoint(root.node.right, mid + l//2 + tab))
            if len(q)>0:
                s = s+ SEP + plot_tree(q)
            return s
        if self.root is not None:
            return plot_tree(roots)
        else:
            return ""

    def insert(self, value: Any)->node:
        """
        Вставка значения в дерево
        """
        def insert_value(root:self.node, value: Any)->self.node:
            if value<root.value:
                if root.left:
                    return insert_value(root.left, value)
                else:
                    node = self.node(value)
                    root.left = node
                    return node
            elif value>root.value:
                if root.right:
                    return insert_value(root.right, value)
                else:
                    node = self.node(value)
                    root.right = node
                    return node
            return root
        if self.root is not None:
            return insert_value(self.root, value)
        else:
            self.root = self.node(value)
            return self.root
    
    def search(self, value)->Union[SearchResult,None]:
        def search_value(root: self.node, value: Any, parent: Optional[self.node], order: Optional[str])->Union[SearchResult,None]:
            """
            Поиск по дереву
            с костылём для удобства возврата родителя
            TODO: выкинуть костыль, поменяв глубину сравнений
            """
            if root.value>value:
                if root.left:
                    return search_value(root.left, value, root, 'left')
                else:
                    return None
            elif root.value<value:
                if root.right:
                    return search_value(root.right, value, root, 'right')
                else:
                    return None
            elif root.value==value:
                return SearchResult(root, parent, order)
        if self.root is not None:
            return search_value(self.root, value, None, None)
        else:
            return None
    
    def __contains__(self, value)->bool:
        if self.search(value) is not None:
            return True
        else:
            return False

    def delete(self, value: Any)->None:
        """
        Удаление значения из дерева
        """
        def delete_item(item:self.node, parent:self.node, order)->None:
            if item.right:
                # move the left tree into the right
                if item.left:
                    right_subtree = BST(item.right)
                    new_left_subtree = right_subtree.insert(item.left.value)
                    if item.left.left:
                        new_left_subtree.left = item.left.left
                    if item.left.right:
                        new_left_subtree.right = item.left.right
                # set right tree inplace
                setattr(parent, order, item.right)
            elif item.left:
                setattr(parent, order, item.left)
            # if the item does not have any children
            # just remove the item
            else:
                setattr(parent, order, None)
        if self.root is not None:
            if self.root.value==value:
                fake_root = self.node(value-1) # TODO: add some care about "overflow"
                fake_root.right = self.root
                delete_item(self.root, fake_root, 'right')
                self.root = fake_root.right
            else:
                root = self.search(value)
                if root:
                    delete_item(root.node, root.parent, root.order)

    def traverse(self):
        """
        Обход слева направо
        """
        def traverse_ltr(root):
            if root.left:
                yield from traverse_ltr(root.left)
            yield root.value
            if root.right:
                yield from traverse_ltr(root.right)
        if self.root is not None:
            return traverse_ltr(self.root)
        else:
            return []

    def __add__(self, other):
        """
            Сложение a.k.a. конкатенация
            двух деревьев
        """
        from copy import deepcopy
        res = deepcopy(self)
        for i in other.traverse():
            if i not in res:
                res.insert(i)
        return res