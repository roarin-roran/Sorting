import unittest
from Support import ListSlice
from Tests import Test_Sorters
from Mergers import Merger_Adaptive
from Merger_IPQs import MergerIPQ_Dummy


class Test_Mergers(unittest.TestCase):

    def test_adaptive_sort(self, merger_ipq_init=False):
        self.prototype_test(Merger_Adaptive.Merger_Adaptive, merger_ipq_init)

    def prototype_test(self,
                       merger_init,
                       merger_ipq_init=False):
        if merger_ipq_init:
            self.merger_ipq_init = merger_ipq_init
        else:
            self.merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(self.merger_ipq_init, merger_init)

        self.merge_two(merger_init)

        self.merge_three_variable_lengths(merger_init)

    def merge_two(self, merger_init):
        two_runs = [2, 3, 0, 1]
        run_1 = ListSlice.ListSlice(two_runs, 0, 2)
        run_2 = ListSlice.ListSlice(two_runs, 2, 4)

        write_list_slice = ListSlice.ListSlice([-1, -1, -1, -1], 0, 4)

        our_merger = merger_init([run_1, run_2], write_list_slice)
        our_merger.merge()

        self.assertEqual(write_list_slice.list, sorted(write_list_slice.list))

    def merge_three_variable_lengths(self, merger_init):
        three_runs = [7, 0, 2, 4, 1, 3, 5, 6]
        run_1 = ListSlice.ListSlice(three_runs, 0, 1)
        run_2 = ListSlice.ListSlice(three_runs, 1, 4)
        run_3 = ListSlice.ListSlice(three_runs, 4, 8)

        write_list_slice = ListSlice.ListSlice([-1] * 7, 0, 7)

        our_merger = merger_init([run_1, run_2, run_3], write_list_slice)
        our_merger.merge()

        self.assertEqual(write_list_slice.list, sorted(write_list_slice.list))


if __name__ == '__main__':
    unittest.main()
