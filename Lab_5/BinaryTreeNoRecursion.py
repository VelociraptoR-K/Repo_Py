from collections import deque

def left_branch_other(root:int)->int:
    return root + 135

def right_branch_other(root:int)->int:
    return root ** 3

def gen_bin_tree(height: int = 2, root: int = 3, left_branch=lambda l_r: l_r + 2, right_branch=lambda r_r: r_r * 3) -> dict:
    """Генерирует бинарное дерево в виде словаря.
        Каждый узел: {корень: [левый потомок, правый потомок]}
        Листья: {значение: []}"""
    if height < 0:
        return 'Вершина дерева должна быть >= 0'
    # Создаем листья (нижний уровень)
    res = {}
    queue = deque([(root, 0)])
    while queue:
        value, level = queue.popleft()
        if level == height:
            res[value] = {value: []}
        else:
            l_b = left_branch(value)
            r_b = right_branch(value)
            queue.append((l_b, level + 1))
            queue.append((r_b, level + 1))

    # Строим дерево снизу вверх
    for level in range(height - 1, -1, -1):
        current_nodes = {}
        queue = deque([(root, 0)])
        while queue:
            value, current_level = queue.popleft()
            l_b = left_branch(value)
            r_b = right_branch(value)
            if current_level == level:
                current_nodes[value] = {value: [res[l_b], res[r_b]]}
            elif current_level < level:
                queue.append((l_b, current_level + 1))
                queue.append((r_b, current_level + 1))
        res = current_nodes
    return res[root]

def gen_bin_tree_tuple(height: int = 1, root: int = 3, left_branch=lambda l_r: l_r + 2, right_branch=lambda r_r: r_r * 3) -> tuple:
    """Генерирует бинарное дерево в виде словаря.
        Каждый узел: (корень: [левый потомок, правый потомок])
        Листья: (значение: [])"""
    if height < 0:
        return 'Вершина дерева должна быть >= 0'
    # Создаем листья (нижний уровень)
    res = {}
    queue = deque([(root, 0)])
    while queue:
        value, level = queue.popleft()
        if level == height:
            res[value] = f"({value}: [])"
        else:
            l_b = left_branch(value)
            r_b = right_branch(value)
            queue.append((l_b, level + 1))
            queue.append((r_b, level + 1))

    # Строим дерево снизу вверх
    for level in range(height - 1, -1, -1):
        current_nodes = {}
        queue = deque([(root, 0)])
        while queue:
            value, current_level = queue.popleft()
            l_b = left_branch(value)
            r_b = right_branch(value)
            if current_level == level:
                current_nodes[value] = f"({value}: [{res[l_b]}, {res[r_b]}])"
            elif current_level < level:
                queue.append((l_b, current_level + 1))
                queue.append((r_b, current_level + 1))
        res = current_nodes
    return res[root]
