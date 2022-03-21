import random
import unittest
from Sorters import Sorter_Adaptive, Sorter_BottomUp, Sorter_LibraryMethods
from Mergers import Merger_Adaptive
from Merger_IPQs import MergerIPQ_Dummy


class Test_Sorters(unittest.TestCase):
    def test_sorter_adaptive(self,
                             merger_ipq_init=False,
                             merger_init=False):
        self.prototype_test(Sorter_Adaptive.Sorter_PingPong_Adaptive, merger_ipq_init, merger_init)

    def test_sorter_bottom_up(self,
                              merger_ipq_init=False,
                              merger_init=False):
        self.prototype_test(Sorter_BottomUp.Sorter_PingPong_BottomUp, merger_ipq_init, merger_init)

    def test_sorter_default(self):
        self.prototype_test(Sorter_LibraryMethods.Sorter_Default)

    def prototype_test(self, sorter_init,
                       merger_ipq_init=False,
                       merger_init=False):
        self.set_methods_used(merger_ipq_init, merger_init)
        self.sorter_init = sorter_init

        self.sort_and_test_up_to_power(4)

    # passes the ipq and merger selection, or sets sensible defaults
    def set_methods_used(self, merger_ipq_init, merger_init):
        if merger_ipq_init:
            self.merger_ipq_init = merger_ipq_init
        else:
            self.merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        if merger_init:
            self.merger_init = merger_init
        else:
            self.merger_init = Merger_Adaptive.Merger_Adaptive

    def sort_and_test_up_to_power(self, max_power):
        for power in range(1, max_power):
            self.sort_n_inputs(n=10**power)

    def sort_n_inputs(self, n):
        random.seed(n)

        random_input = list(range(n))
        sorted_input = random_input.copy()

        for k in range(2, 9):
            random.shuffle(random_input)

            sorter = self.sorter_init(random_input, k,
                                      merger_ipq_init=self.merger_ipq_init,
                                      merger_init=self.merger_init)

            # note that sort is called by get_sorted_list, so sort is tested implicitly here
            self.assertEqual(sorter.get_input_list(), random_input)
            self.assertEqual(sorter.get_sorted_list(), sorted_input)


if __name__ == '__main__':
    unittest.main()
