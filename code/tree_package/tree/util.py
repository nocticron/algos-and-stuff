"""
    Various utilities for binary trees
"""

def max_tree_height(root)->int:
    """
        Calculates the maximum tree height
    """
    if root is not None:
        res = 1
        l = 0
        r = 0
        if root.left is not None:
            l = max_tree_height(root.left)
        if root.right is not None:
            r = max_tree_height(root.right)
        return res + max(l, r)
    else:
        return 0

def calculate_height_diff(root)->int:
    """
        Calculates the height difference 
        between the left and right subtrees
        returns height(right)-height(left)
    """
    if root is not None:
        return max_tree_height(root.right) - max_tree_height(root.left)
    else:
        return 0