import unittest
from collections import namedtuple


def gen_bin_tree(height: int = 5, root: int = 6) -> dict:
    """
    Генерирует бинарное дерево рекурсивным способом.

    Args:
        height: Высота дерева (по умолчанию 5).
        root: Значение корневого узла (по умолчанию 6).

    Returns:
        Словарь, представляющий бинарное дерево с ключами:
        'value', 'left', 'right'.
    """
    if height == 0:
        return None

    left_value = (root * 2) - 2
    right_value = root + 4

    return {
        "value": root,
        "left": gen_bin_tree(height - 1, left_value),
        "right": gen_bin_tree(height - 1, right_value),
    }


def print_tree(tree: dict, indent: int = 0) -> None:
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
        """Корень дерева должен быть 6."""
        tree = gen_bin_tree()
        self.assertEqual(tree["value"], 6)

    def test_left_child(self):
        """Левый потомок корня = (6*2)-2 = 10."""
        tree = gen_bin_tree()
        self.assertEqual(tree["left"]["value"], 10)

    def test_right_child(self):
        """Правый потомок корня = 6+4 = 10... нет = 10."""
        tree = gen_bin_tree()
        self.assertEqual(tree["right"]["value"], 10)

    def test_height_1(self):
        """При высоте 1 потомков нет."""
        tree = gen_bin_tree(height=1, root=6)
        self.assertIsNone(tree["left"])
        self.assertIsNone(tree["right"])

    def test_height_0(self):
        """При высоте 0 дерево пустое."""
        tree = gen_bin_tree(height=0, root=6)
        self.assertIsNone(tree)

    def test_custom_root(self):
        """Проверка с другим корнем."""
        tree = gen_bin_tree(height=2, root=4)
        self.assertEqual(tree["value"], 4)
        self.assertEqual(tree["left"]["value"], (4 * 2) - 2)   # 6
        self.assertEqual(tree["right"]["value"], 4 + 4)         # 8

    def test_second_level_left(self):
        """Второй уровень слева: left of left."""
        tree = gen_bin_tree()
        left = tree["left"]["value"]         # 10
        left_left = tree["left"]["left"]["value"]
        self.assertEqual(left_left, (left * 2) - 2)  # (10*2)-2 = 18


unittest.main(argv=[''], verbosity=2, exit=False)