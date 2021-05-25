"""
    Simple module to spawn tree turning functions
"""
LEFT = "left"
RIGHT = "right"
opposites = {
    LEFT: RIGHT,
    RIGHT: LEFT
}
def turn(how=LEFT, inplace=False):
    """
        Gives you a function which turns a tree
        ('left' or 'right')
    """
    def t(root):
        oppose = opposites[how]
        if (r:=getattr(root, oppose)) is not None:
            t = getattr(getattr(root, oppose), how)
            setattr(root, oppose, t)
            setattr(r, how, root)
            return r
        else:
            return root

    if inplace:
        return t
    else:
        from copy import deepcopy
        def t_copy(root):
            rt = deepcopy(root)
            return t(rt)
        return t_copy

def grosser_turn(how=LEFT, inplace=False):
    """
        Gives you a function which makes a grosser tree turn
    """
    def t(root):
        oppose = opposites[how]
        if (c:=getattr(getattr(root, oppose), how)) is not None:
            a = root
            b = getattr(root, oppose)
            setattr(a, oppose, getattr(c, how))
            setattr(b, how, getattr(c, oppose))
            setattr(c, how, a)
            setattr(c, oppose, b)
            return c
        else:
            return root
    if inplace:
        return t
    else:
        from copy import deepcopy
        def t_copy(root):
            rt = deepcopy(root)
            return t(rt)
        return t_copy
