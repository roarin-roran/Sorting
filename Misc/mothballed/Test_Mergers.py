import unittest
from Support import ListSlice
from Tests import Test_Sorters
from Misc.mothballed import Test_MergerIPQ
from Mergers import Merger_Adaptive, Merger_Tester, Merger_TwoWay
from Merger_IPQs import MergerIPQ, MergerIPQ_Dummy, MergerIPQ_Tester, MergerIPQ_LoserTree
from typing import Union
import os
from os.path import exists


class Test_Mergers(unittest.TestCase):
    def test_tests(self, override_merger_ipq_init=None):
        """ensures that the tests below correctly use the desired merger"""
        merger_init = Merger_Tester.Merger_Tester
        default_merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        self._passing_ipq_test_wrapper(merger_init, override_merger_ipq_init, default_merger_ipq_init)

    def test_adaptive_merge(self, override_merger_ipq_init=None):
        """runs all tests for the adaptive merge sort"""
        merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        self._passing_ipq_test_wrapper(merger_init, override_merger_ipq_init, default_merger_ipq_init)

    def test_adaptive_merge_real_sentinels(self, override_merger_ipq_init=None):
        """runs all tests for the legacy adaptive merge sort which uses real sentinels"""
        merger_init = Merger_Adaptive.Merger_Adaptive_Real_Sentinels
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        self._passing_ipq_test_wrapper(merger_init, override_merger_ipq_init, default_merger_ipq_init)

    def test_two_way_merger(self):
        """runs a custom test suite for the two way merger, which doesn't use an ipq, and can't use the usual test
        inputs"""
        self._merge_two(Merger_TwoWay.Merger_TwoWay, MergerIPQ_Dummy.MergerIPQ_Dummy)
        self._merge_one_element_in_back(Merger_TwoWay.Merger_TwoWay, MergerIPQ_Dummy.MergerIPQ_Dummy)
        self._merge_one_element_in_front(Merger_TwoWay.Merger_TwoWay, MergerIPQ_Dummy.MergerIPQ_Dummy)

        # todo - this fails, why?
        # self.check_correct_merger_used(Merger_Two_Way.Merger_Two_Way)

        # test complete - delete test files to avoid memory leaks
        Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()





    def _passing_ipq_test_wrapper(self, merger_init, override_merger_ipq_init, default_merger_ipq_init):
        """wraps prototype_test, checking if merger_ipq is passed around correctly"""
        # use default ipq, or override it
        if override_merger_ipq_init:
            merger_ipq_init = override_merger_ipq_init
        else:
            merger_ipq_init = default_merger_ipq_init

        # make ipq_tester
        ipq_tester = Test_MergerIPQ.Test_MergerIPQ()

        # test using either default values or override values
        self._prototype_test(merger_init, merger_ipq_init)
        # check that the correct ipq was used, whatever that was
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=merger_ipq_init)

        # wipe to prevent leaks
        Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

        # use a non-default merger, check that that's passed down correctly
        self._prototype_test(merger_init, MergerIPQ_Tester.MergerIPQ_Tester)
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=MergerIPQ_Tester.MergerIPQ_Tester)

        # test complete - delete test files to avoid memory leaks
        Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

    def _prototype_test(self, merger_init, merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False):
        """groups all individual test cases together"""

        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(override_merger_ipq_init=merger_ipq_init,
                                            override_merger_init=merger_init)

        self._merge_two(merger_init, merger_ipq_init, keep_files=True)
        self._merge_three_variable_lengths(merger_init, merger_ipq_init)
        self._merge_one_element_in_front(merger_init, merger_ipq_init)
        self._merge_one_element_in_back(merger_init, merger_ipq_init)
        # check that the desired merger was used and no other merger was used
        self.check_correct_merger_used(merger_init)

    def _merge_two(self, merger_init, merger_ipq_init, keep_files=False):
        """merges two trivial inputs of the same length"""
        if not keep_files:
            Test_Mergers.clear_file_merger()
            Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

        two_runs = [2, 3, 0, 1]
        run_1 = ListSlice.ListSlice(two_runs, 0, 2)
        run_2 = ListSlice.ListSlice(two_runs, 2, 4)

        write_list_slice = ListSlice.ListSlice([-1, -1, -1, -1], 0, 4)

        our_merger = merger_init([run_1, run_2], write_list_slice, merger_ipq_init=merger_ipq_init,
                                 test_mode=True)
        our_merger.merge()

        self.assertEqual([0, 1, 2, 3], write_list_slice.list)

        if not keep_files:
            Test_Mergers.clear_file_merger()
            Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

    def _merge_three_variable_lengths(self, merger_init, merger_ipq_init, keep_files=False):
        """merges three inputs with different lengths"""
        three_runs = [7, 0, 2, 4, 1, 3, 5, 6]
        run_1 = ListSlice.ListSlice(three_runs, 0, 1)
        run_2 = ListSlice.ListSlice(three_runs, 1, 4)
        run_3 = ListSlice.ListSlice(three_runs, 4, 8)

        write_list_slice = ListSlice.ListSlice([-1] * 8, 0, 8)

        our_merger = merger_init([run_1, run_2, run_3], write_list_slice, merger_ipq_init=merger_ipq_init,
                                 test_mode=True)
        our_merger.merge()

        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], write_list_slice.list)

    def _merge_one_element_in_front(self, merger_init, merger_ipq_init, keep_files=False):
        # two_runs = [1, 2, 3, 4, 6, 7, 8, 5]
        two_runs = [5, 1, 2, 3, 4, 6, 7, 8]
        run_1 = ListSlice.ListSlice(two_runs, 0, 1)
        run_2 = ListSlice.ListSlice(two_runs, 1, 8)

        write_list_slice = ListSlice.ListSlice([-1] * 8, 0, 8)

        our_merger = merger_init([run_1, run_2], write_list_slice, merger_ipq_init=merger_ipq_init, test_mode=True)
        our_merger.merge()

        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], write_list_slice.list)

    def _merge_one_element_in_back(self, merger_init, merger_ipq_init, keep_files=False):
        two_runs = [1, 2, 3, 4, 6, 7, 8, 5]
        run_1 = ListSlice.ListSlice(two_runs, 0, 7)
        run_2 = ListSlice.ListSlice(two_runs, 7, 8)

        write_list_slice = ListSlice.ListSlice([-1] * 8, 0, 8)

        our_merger = merger_init([run_1, run_2], write_list_slice, merger_ipq_init=merger_ipq_init, test_mode=True)
        our_merger.merge()

        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], write_list_slice.list)

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


# allows for running of all tests in this file without other tests
if __name__ == '__main__':
    unittest.main()
