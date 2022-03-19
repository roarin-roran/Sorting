import unittest
import Sorter_Adaptive
import Sorter_BottomUp
import random


class Test_Sorters(unittest.TestCase):
    def test_sorter_adaptive(self):
        self.sorter = Sorter_Adaptive.Sorter_PingPong_Adaptive

        self.sort_and_test_up_to_power(4)

    def test_sorter_bottom_up(self):
        self.sorter = Sorter_BottomUp.Sorter_PingPong_BottomUp

        self.sort_and_test_up_to_power(4)

    def sort_and_test_up_to_power(self, max_power):
        for power in range(1, max_power):
            self.sort_n_inputs(n=10**power)

    def sort_n_inputs(self, n=1):
        random.seed(n)

        random_input = list(range(n))
        sorted_input = random_input.copy()

        for k in range(2, 9):
            random.shuffle(random_input)

            sorter = self.sorter(random_input, k)

            # note that sort is called by get_sorted_list, so sort is tested implicitly here
            self.assertEqual(sorter.get_input_list(), random_input)
            self.assertEqual(sorter.get_sorted_list(), sorted_input)


if __name__ == '__main__':
    unittest.main()
