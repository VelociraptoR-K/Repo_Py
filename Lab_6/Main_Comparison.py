from collections import deque
import timeit
import matplotlib.pyplot as plt

def left_branch(root:int)->int:
    """Вычисляет значение левого потомка."""
    return root + 2

def right_branch(root:int)->int:
    """Вычисляет значение правого потомка."""
    return root * 3

def build_tree_recursive(height: int = 4, root: int = 3, l_b:int=left_branch, r_b:int=right_branch) -> dict:
    """Генерирует бинарное дерево в виде словаря.
        Каждый узел: {корень: [левый потомок, правый потомок]}
        Листья: {значение: []}"""
    if height < 0:
        return 'Вершина дерева должна быть >= 0'
    if height == 0:
        return {root: []}
    left_b = l_b(root)
    right_b = r_b(root)
    left_leaf = build_tree_recursive(height - 1, left_b, l_b, r_b)
    right_leaf = build_tree_recursive(height - 1, right_b, l_b, r_b)
    return {root: [left_leaf, right_leaf]}

def build_tree_iterative(height: int = 4, root: int = 3, left_branch=lambda l_r: l_r + 2, right_branch=lambda r_r: r_r * 3) -> dict:
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

def benchmark(func, h, number=1, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(h), number=number, repeat=repeat)
    return min(times)

def main():
    # фиксированный набор данных
    test_data = list(range(20))

    res_recursive = []
    res_iterative = []

    for h in test_data: # h - height
      res_recursive.append(benchmark(build_tree_recursive, h))
      res_iterative.append(benchmark(build_tree_iterative, h))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивное построение")
    plt.plot(test_data, res_iterative, label="Итеративное построение")
    plt.xlabel("height")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного способа построения")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

