import unittest
from Support import ListSlice
from Tests import Test_Sorters
from Mergers import Merger_Adaptive


class Test_Mergers(unittest.TestCase):

    def test_merge_two(self):
        two_runs = [2, 3, 0, 1]
        run_1 = ListSlice.ListSlice(two_runs, 0, 2)
        run_2 = ListSlice.ListSlice(two_runs, 2, 4)

        write_list_slice = ListSlice.ListSlice([-1, -1, -1, -1], 0, 4)

        # fiddle with this when more mergers are added
        our_merger = Merger_Adaptive.Merger_Adaptive([run_1, run_2], write_list_slice)
        output = our_merger.merge()

        self.assertEqual(output.list, sorted(write_list_slice.list))

    def test_merge_three_variable_lengths(self):
        three_runs = [7, 0, 2, 4, 1, 3, 5, 6]
        run_1 = ListSlice.ListSlice(three_runs, 0, 1)
        run_2 = ListSlice.ListSlice(three_runs, 1, 4)
        run_3 = ListSlice.ListSlice(three_runs, 4, 8)

        write_list_slice = ListSlice.ListSlice([-1] * 7, 0, 7)

        # fiddle with this when more mergers are added
        our_merger = Merger_Adaptive.Merger_Adaptive([run_1, run_2, run_3], write_list_slice)
        output = our_merger.merge()

        self.assertEqual(output.list, sorted(write_list_slice.list))

    def test_adaptive_sort(self):
        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(merger_init=Merger_Adaptive.Merger_Adaptive)


if __name__ == '__main__':
    unittest.main()
