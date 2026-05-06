import unittest
from collections import deque
from typing import Callable


def gen_bin_tree(
    height: int = 5,
    root: int = 6,
    left_branch: Callable[[int], int] = lambda r: (r * 2) - 2,
    right_branch: Callable[[int], int] = lambda r: r + 4,
) -> dict:
    """
    Генерирует бинарное дерево нерекурсивным способом (с использованием очереди).

    Args:
        height: Высота дерева (по умолчанию 5).
        root: Значение корневого узла (по умолчанию 6).
        left_branch: Лямбда-функция для вычисления левого потомка.
        right_branch: Лямбда-функция для вычисления правого потомка.

    Returns:
        Словарь, представляющий бинарное дерево с ключами:
        'value', 'left', 'right'.
    """
    if height == 0:
        return None

    root_node = {"value": root, "left": None, "right": None}

    # Очередь: узел и текущая высота
    queue = deque()
    queue.append((root_node, 1))

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


def print_tree(tree: dict | None, indent: int = 0) -> None:
    """
    Выводит дерево в читаемом виде.

    Args:
        tree: Словарь дерева.
        indent: Отступ для визуализации уровня.
    """
    if tree is None:
        return
    print(" " * indent + str(tree["value"]))
    print_tree(tree["left"], indent + 4)
    print_tree(tree["right"], indent + 4)


#ТЕСТЫ
class TestGenBinTree(unittest.TestCase):

    def test_root_value(self):
        """Корень должен быть 6."""
        tree = gen_bin_tree()
        self.assertEqual(tree["value"], 6)

    def test_left_child_default(self):
        """Левый потомок корня = (6*2)-2 = 10."""
        tree = gen_bin_tree()
        self.assertEqual(tree["left"]["value"], 10)

    def test_right_child_default(self):
        """Правый потомок корня = 6+4 = 10."""
        tree = gen_bin_tree()
        self.assertEqual(tree["right"]["value"], 10)

    def test_height_1_no_children(self):
        """При высоте 1 нет потомков."""
        tree = gen_bin_tree(height=1)
        self.assertIsNone(tree["left"])
        self.assertIsNone(tree["right"])

    def test_height_0_returns_none(self):
        """При высоте 0 дерево пустое."""
        tree = gen_bin_tree(height=0)
        self.assertIsNone(tree)

    def test_custom_lambda(self):
        """Проверка с пользовательскими лямбда-функциями."""
        tree = gen_bin_tree(
            height=2,
            root=10,
            left_branch=lambda r: r * 2,
            right_branch=lambda r: r + 1,
        )
        self.assertEqual(tree["left"]["value"], 20)
        self.assertEqual(tree["right"]["value"], 11)

    def test_second_level(self):
        """Проверка второго уровня дерева."""
        tree = gen_bin_tree(height=3)
        left_val = tree["left"]["value"]          # 10
        left_left = tree["left"]["left"]["value"] # (10*2)-2 = 18
        self.assertEqual(left_left, (left_val * 2) - 2)


unittest.main(argv=[''], verbosity=2, exit=False)