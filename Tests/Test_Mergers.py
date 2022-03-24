import unittest
from Support import ListSlice
from Tests import Test_Sorters, Test_MergerIPQ
from Mergers import Merger_Adaptive, Merger_Tester
from Merger_IPQs import MergerIPQ, MergerIPQ_Dummy, MergerIPQ_Tester
from typing import Union
import os
from os.path import exists


class Test_Mergers(unittest.TestCase):
    def test_tests(self, override_merger_ipq_init=False):
        """ensures that the tests below correctly use the desired merger"""
        merger_init = Merger_Tester.Merger_Tester
        default_merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        self.passing_ipq_test_wrapper(merger_init, override_merger_ipq_init, default_merger_ipq_init)

    def test_adaptive_merge(self, override_merger_ipq_init=False):
        """runs all tests for the adaptive merge sort"""
        merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        self.passing_ipq_test_wrapper(merger_init, override_merger_ipq_init, default_merger_ipq_init)

    def passing_ipq_test_wrapper(self, merger_init, override_merger_ipq_init, default_merger_ipq_init):
        """wraps prototype_test, checking if merger_ipq is passed around correctly"""
        # use default ipq, or override it
        if override_merger_ipq_init:
            merger_ipq_init = override_merger_ipq_init
        else:
            merger_ipq_init = default_merger_ipq_init

        # make ipq_tester
        ipq_tester = Test_MergerIPQ.Test_MergerIPQ()

        print("\n\t\tNON TEST MERGER\n")
        # test using either default values or override values
        self.prototype_test(merger_init, merger_ipq_init)
        # check that the correct ipq was used, whatever that was
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=merger_ipq_init)

        print("\n\t\tTEST MERGER\n")
        # use a non-default merger, check that that's passed down correctly
        self.prototype_test(merger_init, MergerIPQ_Tester.MergerIPQ_Tester)
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=MergerIPQ_Tester.MergerIPQ_Tester)

    def prototype_test(self, merger_init, merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False):
        """groups all individual test cases together"""

        print("\n\t\tTEST BY USING\n")
        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(override_merger_ipq_init=merger_ipq_init,
                                            override_merger_init=merger_init)

        # todo - this seems a little low
        Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

        print("\n\t\tTEST WITH FIXED VALUES\n")

        self.merge_two(merger_init, merger_ipq_init)

        self.merge_three_variable_lengths(merger_init, merger_ipq_init)
        # check that the desired merger was used and no other merger was used
        self.check_correct_merger_used(merger_init)

    def merge_two(self, merger_init, merger_ipq_init):
        """merges two trivial inputs of the same length"""
        two_runs = [2, 3, 0, 1]
        run_1 = ListSlice.ListSlice(two_runs, 0, 2)
        run_2 = ListSlice.ListSlice(two_runs, 2, 4)

        write_list_slice = ListSlice.ListSlice([-1, -1, -1, -1], 0, 4)

        our_merger = merger_init([run_1, run_2], write_list_slice, merger_ipq_init=merger_ipq_init,
                                 test_mode=True)
        our_merger.merge()

        self.assertEqual(write_list_slice.list, sorted(write_list_slice.list))

    def merge_three_variable_lengths(self, merger_init, merger_ipq_init):
        """merges three inputs with different lengths"""
        three_runs = [7, 0, 2, 4, 1, 3, 5, 6]
        run_1 = ListSlice.ListSlice(three_runs, 0, 1)
        run_2 = ListSlice.ListSlice(three_runs, 1, 4)
        run_3 = ListSlice.ListSlice(three_runs, 4, 8)

        write_list_slice = ListSlice.ListSlice([-1] * 7, 0, 7)

        our_merger = merger_init([run_1, run_2, run_3], write_list_slice, merger_ipq_init=merger_ipq_init,
                                 test_mode=True)
        our_merger.merge()

        self.assertEqual(write_list_slice.list, sorted(write_list_slice.list))

    def check_correct_merger_used(self, correct_merger_init):
        """checks that the correct merger is the only merger that's been used since the last wipe"""
        blank_merger = correct_merger_init([], ListSlice.ListSlice([], 0, 0))
        f_r = open("test_options_merger.txt", "r")

        correct_answer = str(blank_merger.option_code)

        for entry in f_r:
            given_answer = entry[0]
            self.assertEqual(correct_answer, given_answer)

        f_r.close()

    @staticmethod
    def print_options_merger():
        """prints all mergers used since the last wipe"""
        if exists("test_options_merger.txt"):
            f_r = open("test_options_merger.txt", "r")
            for entry in f_r:
                print(entry)

            f_r.close()

    @staticmethod
    def clear_file_merger():
        """wipes the file which records which mergers have been used"""
        if exists("test_options_merger.txt"):
            os.remove("test_options_merger.txt")


if __name__ == '__main__':
    unittest.main()
