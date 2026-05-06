import unittest
import timeit
import matplotlib.pyplot as plt
from collections import deque
from typing import Callable


# RECURSIVE 
def build_tree_recursive(
    height: int = 5,
    root: int = 6,
    left_branch: Callable[[int], int] = lambda r: (r * 2) - 2,
    right_branch: Callable[[int], int] = lambda r: r + 4,
) -> dict | None:
    """
    Строит бинарное дерево рекурсивным способом.

    Args:
        height: Высота дерева.
        root: Значение корневого узла.
        left_branch: Функция вычисления левого потомка.
        right_branch: Функция вычисления правого потомка.

    Returns:
        Словарь с ключами 'value', 'left', 'right' или None если высота 0.
    """
    if height == 0:
        return None
    return {
        "value": root,
        "left": build_tree_recursive(height - 1, left_branch(root), left_branch, right_branch),
        "right": build_tree_recursive(height - 1, right_branch(root), left_branch, right_branch),
    }


# ITERATIVE 
def build_tree_iterative(
    height: int = 5,
    root: int = 6,
    left_branch: Callable[[int], int] = lambda r: (r * 2) - 2,
    right_branch: Callable[[int], int] = lambda r: r + 4,
) -> dict | None:
    """
    Строит бинарное дерево нерекурсивным способом (через очередь).

    Args:
        height: Высота дерева.
        root: Значение корневого узла.
        left_branch: Функция вычисления левого потомка.
        right_branch: Функция вычисления правого потомка.

    Returns:
        Словарь с ключами 'value', 'left', 'right' или None если высота 0.
    """
    if height == 0:
        return None

    root_node = {"value": root, "left": None, "right": None}
    queue = deque([(root_node, 1)])

    while queue:
        node, current_height = queue.popleft()
        if current_height < height:
            left_val = left_branch(node["value"])
            right_val = right_branch(node["value"])
            node["left"] = {"value": left_val, "left": None, "right": None}
            node["right"] = {"value": right_val, "left": None, "right": None}
            queue.append((node["left"], current_height + 1))
            queue.append((node["right"], current_height + 1))

    return root_node


#  СРАВНЕНИЕ ВРЕМЕНИ 
def compare_performance(
    max_height: int = 12,
    root: int = 6,
    repetitions: int = 100,
) -> None:
    """
    Сравнивает время работы рекурсивной и нерекурсивной реализаций.
    Строит график зависимости времени от высоты дерева.

    Args:
        max_height: Максимальная высота для тестирования.
        root: Корень дерева.
        repetitions: Количество повторений для timeit.
    """
    heights = list(range(1, max_height + 1))
    recursive_times = []
    iterative_times = []

    for h in heights:
        t_rec = timeit.timeit(
            lambda: build_tree_recursive(h, root),
            number=repetitions
        )
        t_iter = timeit.timeit(
            lambda: build_tree_iterative(h, root),
            number=repetitions
        )
        recursive_times.append(t_rec)
        iterative_times.append(t_iter)
        print(f"Height {h:2d} | Recursive: {t_rec:.5f}s | Iterative: {t_iter:.5f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(heights, recursive_times, label="Recursive", marker="o", color="blue")
    plt.plot(heights, iterative_times, label="Iterative", marker="s", color="orange")
    plt.xlabel("Высота дерева (Height)")
    plt.ylabel("Время построения (сек)")
    plt.title("Сравнение рекурсивного и нерекурсивного построения бинарного дерева\nVariant 6: root=6, left=(r*2)-2, right=r+4")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("tree_comparison.png")
    # plt.show()  ← معلّق عشان ما يتعارض مع PyCharm
    print("\nГрафик сохранён как tree_comparison.png")


#  ТЕСТЫ 
class TestBuildTree(unittest.TestCase):

    def test_recursive_root(self):
        tree = build_tree_recursive()
        self.assertEqual(tree["value"], 6)

    def test_iterative_root(self):
        tree = build_tree_iterative()
        self.assertEqual(tree["value"], 6)

    def test_recursive_left(self):
        tree = build_tree_recursive()
        self.assertEqual(tree["left"]["value"], 10)  # (6*2)-2

    def test_iterative_left(self):
        tree = build_tree_iterative()
        self.assertEqual(tree["left"]["value"], 10)

    def test_recursive_right(self):
        tree = build_tree_recursive()
        self.assertEqual(tree["right"]["value"], 10)  # 6+4

    def test_iterative_right(self):
        tree = build_tree_iterative()
        self.assertEqual(tree["right"]["value"], 10)

    def test_height_0(self):
        self.assertIsNone(build_tree_recursive(height=0))
        self.assertIsNone(build_tree_iterative(height=0))

    def test_height_1_no_children(self):
        for fn in [build_tree_recursive, build_tree_iterative]:
            tree = fn(height=1)
            self.assertIsNone(tree["left"])
            self.assertIsNone(tree["right"])

    def test_both_same_structure(self):
        """الشجرتان يجب أن تكونا متطابقتين."""
        t_rec = build_tree_recursive(height=4)
        t_iter = build_tree_iterative(height=4)
        self.assertEqual(t_rec, t_iter)


# MAIN 
if __name__ == "__main__":
    import sys
    if "test" in sys.argv:
        unittest.main()
    else:
        compare_performance()