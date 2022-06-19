from Tests import Test, Test_Sorters
from Support import ListSlice
from Merger_IPQs import MergerIPQ, MergerIPQ_Dummy, MergerIPQ_Tester, MergerIPQ_LoserTree
from Mergers import Merger, Merger_Tester, Merger_Adaptive, Merger_TwoWay
from typing import Union
import unittest


class Test_Mergers(Test.Test):
    def __init__(self, merger_init: type(Merger.Merger),
                 test_case,
                 override_merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False,
                 check_ipq_selection=False,
                 check_merger_selection=False):
        super().__init__(check_ipq_selection, check_merger_selection)

        self.test_case = test_case

        self.merger_init = merger_init
        self.override_merger_ipq_init = override_merger_ipq_init

    # * * * * * * ** * * * * * * *
    # * * * * * INPUTS * * * * * *
    # * * * * * * ** * * * * * * *

    def _merge_two(self, merger_ipq_init):
        """merges two trivial inputs of the same length"""
        self.clear_unnecessary_files()

        # define input
        two_runs = [2, 3, 0, 1]
        run_1 = ListSlice.ListSlice(two_runs, 0, 2)
        run_2 = ListSlice.ListSlice(two_runs, 2, 4)
        merge_stack = [run_1, run_2]

        write_list_slice = ListSlice.ListSlice([-1] * 4, 0, 4)

        # merge
        our_merger = self.merger_init(merge_stack, write_list_slice, merger_ipq_init=merger_ipq_init, test_mode=True)
        our_merger.merge()

        # assert answer is correct
        self.test_case.assertEqual([0, 1, 2, 3], write_list_slice.list)

        self.clear_unnecessary_files()

    def _merge_three_variable_lengths(self, merger_ipq_init):
        """merges three inputs with different lengths"""
        self.clear_unnecessary_files()

        # define input
        three_runs = [7, 0, 2, 4, 1, 3, 5, 6]
        run_1 = ListSlice.ListSlice(three_runs, 0, 1)
        run_2 = ListSlice.ListSlice(three_runs, 1, 4)
        run_3 = ListSlice.ListSlice(three_runs, 4, 8)
        merge_stack = [run_1, run_2, run_3]

        write_list_slice = ListSlice.ListSlice([-1] * 8, 0, 8)

        # merge
        our_merger = self.merger_init(merge_stack, write_list_slice, merger_ipq_init=merger_ipq_init, test_mode=True)
        our_merger.merge()

        # assert answer is correct
        self.test_case.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], write_list_slice.list)

        self.clear_unnecessary_files()

    def _merge_one_element_in_front(self, merger_ipq_init):
        """merges a single element into a list, a case that caused bugs in the past"""
        self.clear_unnecessary_files()

        # define input
        two_runs = [5, 1, 2, 3, 4, 6, 7, 8]
        run_1 = ListSlice.ListSlice(two_runs, 0, 1)
        run_2 = ListSlice.ListSlice(two_runs, 1, 8)
        merge_stack = [run_1, run_2]

        write_list_slice = ListSlice.ListSlice([-1] * 8, 0, 8)

        # merge
        our_merger = self.merger_init(merge_stack, write_list_slice, merger_ipq_init=merger_ipq_init, test_mode=True)
        our_merger.merge()

        # assert answer is correct
        self.test_case.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], write_list_slice.list)

        self.clear_unnecessary_files()

    def _merge_one_element_in_back(self, merger_ipq_init):
        """merges a single element into a list, a case that caused bugs in the past"""
        self.clear_unnecessary_files()

        # define input
        two_runs = [1, 2, 3, 4, 6, 7, 8, 5]
        run_1 = ListSlice.ListSlice(two_runs, 0, 7)
        run_2 = ListSlice.ListSlice(two_runs, 7, 8)
        merge_stack = [run_1, run_2]

        write_list_slice = ListSlice.ListSlice([-1] * 8, 0, 8)

        # merge
        our_merger = self.merger_init(merge_stack, write_list_slice, merger_ipq_init=merger_ipq_init, test_mode=True)
        our_merger.merge()

        # assert answer is correct
        self.test_case.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], write_list_slice.list)

        self.clear_unnecessary_files()

    # * * * * * * * * * * * * * *
    # * * * * * UTILITY * * * * *
    # * * * * * * * * * * * * * *

    def _prototype_test(self, merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False):
        """groups all individual test cases together"""

        # clear files on startup, then record the merger selection
        self.clear_unnecessary_files()
        self.check_merger_selection = True

        test_completed = False
        try:
            # 1. use the merger at issue to do a sorting test:
            #    high volume random values, testing for problems caused by this merger
            sorter_tester = Test_Sorters.TestCases()

            sorter_tester.test_element_using_sorter(override_merger_ipq_init=merger_ipq_init,
                                                    override_merger_init=self.merger_init)

            # 2. apply fixed tests - use human generated values to reproduce expected behaviour
            self._merge_two(merger_ipq_init)
            self._merge_three_variable_lengths(merger_ipq_init)
            self._merge_one_element_in_front(merger_ipq_init)
            self._merge_one_element_in_back(merger_ipq_init)

            # 3. check that the desired merger was used and no other merger was used
            self._check_correct_merger_used(self.merger_init)

            test_completed = True
        finally:
            if not test_completed:
                self.test_case.fail(msg="merger test failed to complete")

        # clear files on termination, including the merger selection.
        self.check_merger_selection = False
        self.clear_unnecessary_files()

    def _passing_ipq_test_wrapper(self, override_merger_ipq_init, default_merger_ipq_init):
        """wraps prototype_test, checking if merger_ipq is passed around correctly"""
        # use the default merger IPQ, or override it.
        if override_merger_ipq_init:
            merger_ipq_init = override_merger_ipq_init
        else:
            merger_ipq_init = default_merger_ipq_init

        # wipe to prevent leaks
        self.clear_unnecessary_files()
        self.check_ipq_selection = True

        # test using either default values or override values
        self._prototype_test(merger_ipq_init)
        # check that the correct ipq was used, whatever that was
        self._check_correct_merger_ipq_used(correct_merger_ipq_init=merger_ipq_init)

        # wipe ipq file to prevent leaks
        self.clear_file_ipq()

        # use a non-default merger, check that that's passed down correctly
        self._prototype_test(MergerIPQ_Tester.MergerIPQ_Tester)
        self._check_correct_merger_ipq_used(correct_merger_ipq_init=MergerIPQ_Tester.MergerIPQ_Tester)

        # test complete - delete test files to avoid memory leaks
        self.check_ipq_selection = False
        self.clear_unnecessary_files()

    # * * * * * * * * * * * * * *
    # * * * * * TESTS * * * * * *
    # * * * * * * * * * * * * * *


class TestCases(unittest.TestCase):
    def test_tests(self, override_merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = None):
        """ensures that the tests below correctly use the desired merger"""
        merger_init = Merger_Tester.Merger_Tester
        default_merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        our_tester = Test_Mergers(merger_init, self, default_merger_ipq_init)
        our_tester._passing_ipq_test_wrapper(override_merger_ipq_init, default_merger_ipq_init)

        print("tested merger tests")

    def test_adaptive_merge(self, override_merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = None):
        """runs all tests for the adaptive merge sort"""
        merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        our_tester = Test_Mergers(merger_init, self, default_merger_ipq_init)
        our_tester._passing_ipq_test_wrapper(override_merger_ipq_init, default_merger_ipq_init)

        print("tested adaptive merge - virtual sentinels")

    def test_adaptive_merge_real_sentinels(self, override_merger_ipq_init=None):
        """runs all tests for the legacy adaptive merge sort which uses real sentinels"""
        merger_init = Merger_Adaptive.Merger_Adaptive_Real_Sentinels
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        our_tester = Test_Mergers(merger_init, self, default_merger_ipq_init)
        our_tester._passing_ipq_test_wrapper(override_merger_ipq_init, default_merger_ipq_init)

        print("tested adaptive merge - real sentinels")

    def test_two_way_merger(self):
        """runs a custom test suite for the two way merger, which doesn't use an ipq, and can't use the usual test
        inputs"""
        our_tester = Test_Mergers(Merger_TwoWay.Merger_TwoWay, self, check_merger_selection=True)

        our_tester.clear_unnecessary_files()
        our_tester.check_merger_selection = True

        # wrap the test to prevent failure to run from causing issues
        test_completed = False
        try:
            # note that no ipq is actually used - we just have to give one here.
            our_tester._merge_two(None)
            our_tester._merge_one_element_in_back(None)
            our_tester._merge_one_element_in_front(None)

            our_tester._check_correct_merger_used(Merger_TwoWay.Merger_TwoWay)

            test_completed = True
        finally:
            if not test_completed:
                self.fail(msg="merger test failed to complete")

        self.check_merger_selection = False
        our_tester.clear_unnecessary_files()

        print("tested two way merge")

    # * * * * * *  * * * * * * *
    # * * * * * MAIN * * * * * *
    # * * * * * *  * * * * * * *


if __name__ == "__main__":
    unittest.main()
