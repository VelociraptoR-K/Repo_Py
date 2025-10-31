def left_branch(root:int)->int:
    """Вычисляет значение левого потомка."""
    return root + 2

def right_branch(root:int)->int:
    """Вычисляет значение правого потомка."""
    return root * 3

# всего 2**(n+1) - 1

def gen_bin_tree(height: int = 2, root: int = 3, l_b:int=left_branch, r_b:int=right_branch):
    """Генерирует бинарное дерево в виде словаря.
        Каждый узел: {корень: [левый потомок, правый потомок]}
        Листья: {значение: []}"""
    if height < 0:
        return 'Вершина дерева должна быть >= 0'
    if height == 0:
        return {root: []}
    left_b = l_b(root)
    right_b = r_b(root)
    left_leaf = gen_bin_tree(height - 1, left_b, l_b, r_b)
    right_leaf = gen_bin_tree(height - 1, right_b, l_b, r_b)
    return {root: [left_leaf, right_leaf]}

def gen_bin_tree_tuple(height:int = 1, root:int = 3, l_b:int=left_branch, r_b:int=right_branch):
    """Генерирует бинарное дерево в виде кортежа.
       Каждый узел: (корень: [левый потомок, правый потомок])
       Листья: (значение: [])"""
    if height < 0:
        return 'Вершина дерева должна быть >= 0'
    if height == 0:
        return f"({root}: [])"
    left_b = l_b(root)
    right_b = r_b(root)
    left = gen_bin_tree_tuple(height - 1, left_b, l_b, r_b)
    right = gen_bin_tree_tuple(height - 1, right_b, l_b, r_b)
    return f"({root}: [{left}, {right}])"





