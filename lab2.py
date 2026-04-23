import unittest
import random


def guess_number(number: int, nums: list[int], method: str = "binary") -> tuple[int, int]:
    """
    Угадывает число из списка с помощью выбранного алгоритма.

    Args:
        number: Число, которое нужно угадать.
        nums: Список чисел, в котором происходит угадывание.
        method: Способ угадывания — 'slow' (перебор) или 'binary' (бинарный поиск).

    Returns:
        Кортеж (угаданное число, количество угадываний).
    """
    sorted_nums = sorted(nums)
    attempts = 0

    if method == "slow":
        for n in sorted_nums:
            attempts += 1
            if n == number:
                return (n, attempts)

    elif method == "binary":
        low, high = 0, len(sorted_nums) - 1
        while low <= high:
            attempts += 1
            mid = (low + high) // 2
            if sorted_nums[mid] == number:
                return (sorted_nums[mid], attempts)
            elif sorted_nums[mid] < number:
                low = mid + 1
            else:
                high = mid - 1

    return (-1, attempts)


def get_input_from_user() -> tuple[int, int, int]:
    """
    Вспомогательная функция для получения данных с клавиатуры.

    Returns:
        Кортеж (загаданное число, начало диапазона, конец диапазона).
    """
    start = int(input("Начало диапазона: "))
    end = int(input("Конец диапазона: "))
    number = int(input(f"Введите число от {start} до {end}: "))
    return (number, start, end)


# ТЕСТЫ
class TestGuessNumber(unittest.TestCase):

    def test_binary_example1(self):
        nums = list(range(1, 101))
        result, attempts = guess_number(42, nums, method="binary")
        self.assertEqual(result, 42)
        self.assertLessEqual(attempts, 7)  # log2(100) ≈ 7

    def test_slow_example1(self):
        nums = list(range(1, 101))
        result, attempts = guess_number(1, nums, method="slow")
        self.assertEqual(result, 1)
        self.assertEqual(attempts, 1)

    def test_binary_first(self):
        nums = list(range(1, 11))
        result, _ = guess_number(1, nums, method="binary")
        self.assertEqual(result, 1)

    def test_binary_last(self):
        nums = list(range(1, 11))
        result, _ = guess_number(10, nums, method="binary")
        self.assertEqual(result, 10)

    def test_unsorted_list(self):
        nums = [5, 3, 8, 1, 9, 2]
        result, _ = guess_number(8, nums, method="binary")
        self.assertEqual(result, 8)

    def test_not_found(self):
        nums = list(range(1, 10))
        result, _ = guess_number(99, nums, method="binary")
        self.assertEqual(result, -1)


unittest.main(argv=[''], verbosity=2, exit=False)