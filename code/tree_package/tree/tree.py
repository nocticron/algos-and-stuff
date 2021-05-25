from typing import Iterable, Any, Union, Optional, Tuple
from .node import Node, AVLNode
from .turns import turn, grosser_turn, LEFT, RIGHT

class SearchResult:
    """
    Proxy structure to simplicity of search and deletion
    (saves the parent and child's inheritance order)
    """
    def __init__(self, node, parent, order: str)-> None:
        self.node = node
        self.parent = parent
        self.order = order

class NodePoint:
    """
    Printing proxy object
    adds a node printng offset
    """
    def __init__(self, node, offset: int)-> None:
        self.node = node
        self.offset = offset

class BST:
    """
    Binary search tree
    without subtree balancing
    """
    node = Node
    root = None
    printing_offset = 20

    def __init__(self, data: Any, node_type=None):
        # no strict input check
        # cause of duck typing philosophy
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
                Breadth-first printing
                TODO: compute root offset at the bottom of the tree
                (instead of pre-set printing_offset)
                TODO: make use of collections.deque 
                (instead of q)
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
            Adds value to the tree.
            Make sure it is comparable.
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
        """
            Searches value at the tree.
            Make sure it's comparable.
        """
        def search_value(root: self.node, value: Any, parent: Optional[self.node], order: Optional[str])->Union[SearchResult,None]:
            """
                TODO: get rid of SearchResult proxy
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
        Deletes the item from the tree.
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
            # if we want to delete a root value
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
        Left-to-right traverse.
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
            Tree concatenation.
        """
        from copy import deepcopy
        res = deepcopy(self)
        for i in other.traverse():
            if i not in res:
                res.insert(i)
        return res


class AVLT(BST):
    """
    USSR POWER
    """
    node = AVLNode
    @staticmethod
    def grosser_left(root):
        return grosser_turn(LEFT)(root)
    @staticmethod
    def grosser_right(root):
        return grosser_turn(RIGHT)(root)
    @staticmethod
    def lesser_left(root):
        return turn(LEFT)(root)
    @staticmethod
    def lesser_right(root):
        return turn(RIGHT)(root)

    def balance(self, root):
        """
            Default AVL balancing scheme
        """
        if root.balance==-2:
            if root.left.balance>0:
                root = self.grosser_right(root) 
                root.left.recalculate_height() # left must exist
                root.right.recalculate_height() # right also
                root.recalculate_height()               
            else:
                root = self.lesser_right(root)
                root.right.recalculate_height() # right must exist
                root.recalculate_height()
        elif root.balance==2:
            if root.right.balance<0:
                root = self.grosser_left(root)
                root.left.recalculate_height() # left must exist
                root.right.recalculate_height() # right also
                root.recalculate_height()
            else:
                root = self.lesser_left(root)
                root.left.recalculate_height() # left must exist
                root.recalculate_height()
        return root

    def insert(self, value: Any) -> node:
        """
            Insert an item to the tree.
            Make sure it is comparable.
        """
        def insert_value(root:self.node, value: Any)->Tuple[self.node, int]:
            if value<root.value:
                if root.left is None:
                    root.left = self.node(value)
                else:
                    root.left = insert_value(root.left, value)
            elif value>root.value:
                if root.right is None:
                    root.right = self.node(value)
                else:
                    root.right = insert_value(root.right, value)
            root.recalculate_height()
            return self.balance(root)

        if self.root is not None:
            self.root = insert_value(self.root, value)
        else:
            self.root = self.node(value)
            return self.root

    def delete(self, value):
        """
            Deletes item from the tree.
            Too lazy to impl for now.
            TODO: impl
        """
        raise NotImplementedError