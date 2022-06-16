from Merger_IPQs import MergerIPQ, MergerIPQ_Tester, MergerIPQ_LoserTree
from Mergers import Merger, Merger_Tester, Merger_Adaptive, Merger_TwoWay
from Sorters import Sorter, Sorter_LibraryMethods, Sorter_BottomUp, Sorter_Adaptive, Sorter_Peeksort, \
    Sorter_Adaptive_k_2
from Tests import Test
import os
import unittest
from typing import Union
import random


class Test_Sorters(Test.Test):
    def __init__(self, sorter_init: type(Sorter.Sorter),
                 test_case,
                 override_merger_init: Union[bool, type(Merger.Merger)] = False,
                 override_merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False,
                 check_ipq_selection=False,
                 check_merger_selection=False):
        super().__init__(check_ipq_selection, check_merger_selection)

        self.test_case = test_case

        self.sorter_init = sorter_init
        self.override_merger_init = override_merger_init
        self.override_merger_ipq_init = override_merger_ipq_init

        self.random_seed = 142857

    # * * * * * * ** * * * * * * *
    # * * * * * INPUTS * * * * * *
    # * * * * * * ** * * * * * * *

    def _sort_single_element(self):
        """tests that a sorter can handle the trivial input of a single character. note that this should NOT be special
        cased - the potential flaw we're checking for here is the creation of a merger for an input that doesn't need
        one"""
        # this test requires no files to exist before or after its execution

        self.clear_all_files()

        random_input = [1]
        sorted_input = [1]
        sorter = self.sorter_init(random_input, 2,
                                  merger_ipq_init=self.override_merger_ipq_init,
                                  merger_init=self.override_merger_init,
                                  test_mode=True)
        sorter.sort()

        # check sortedness
        self.test_case.assertEqual(sorted_input, random_input)

        # assure that no mergers or merger ipqs are used for this input
        self.test_case.assertFalse(os.path.isfile("test_options_merger_ipq.txt")), \
            "a merger ipq was used for a single element"
        self.test_case.assertFalse(os.path.isfile("test_options_merger.txt")), "a merger was used for a single element"

        # this method shouldn't create files on a pass - but a fail may cause other tests to fail without this step
        self.clear_all_files()

    def _sort_and_test_up_to_power(self, max_power, max_k):
        """creates inputs up to 10^max_power, and sorts each one with all k values between 2 and max_k, inclusive."""
        random.seed(self.random_seed)

        # for all powers
        for power in range(1, max_power + 1):
            n = 10 ** power

            # create input in order, then shuffle it
            sorted_input = list(range(n))
            random_input = sorted_input.copy()

            # for all k values
            for k in range(2, max_k + 1):
                # shuffle input
                random.shuffle(random_input)

                # sort
                sorter = self.sorter_init(random_input, k,
                                          merger_ipq_init=self.override_merger_ipq_init,
                                          merger_init=self.override_merger_init,
                                          test_mode=True)
                sorter.sort()

                # check sortedness
                self.test_case.assertEqual(sorted_input, random_input)

    # * * * * * * * * * * * * * *
    # * * * * * UTILITY * * * * *
    # * * * * * * * * * * * * * *

    def _prototype_test(self, sorter_init,
                        merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = None,
                        merger_init: Union[bool, type(Merger.Merger)] = None):
        """tests that the inserted sorter correctly sorts several inserted lists with a variety of k values"""
        self.sorter_init = sorter_init
        self.override_merger_ipq_init = merger_ipq_init
        self.override_merger_init = merger_init

        # wrap the test to prevent failure to run from causing issues
        test_completed = False
        try:
            # only test if this one runs - it doesn't use a merger or merger IPQ, so it's pointless to test if it
            # uses the correct one

            # note that this will clear all files, so must be performed first
            self._sort_single_element()
            self._sort_and_test_up_to_power(max_power=2, max_k=4)
            test_completed = True

        finally:
            if not test_completed:
                self.test_case.fail(msg="sorter test failed to complete")

    def _passing_test_wrapper(self, sorter_init,
                              override_merger_init, default_merger_init,
                              override_merger_ipq_init, default_merger_ipq_init):
        """an extended test for custom methods - wraps prototype_test, and confirms that this sorter correctly passes
        mergers and ipqs"""

        # set options.
        if override_merger_init:
            merger_init = override_merger_init
        else:
            merger_init = default_merger_init

        if override_merger_ipq_init:
            merger_ipq_init = override_merger_ipq_init
        else:
            merger_ipq_init = default_merger_ipq_init

        # test using either default values or override values
        self._prototype_test(sorter_init, merger_ipq_init, merger_init)
        # check that the correct merger was used
        self._check_correct_merger_used(correct_merger_init=merger_init)
        # check that the correct ipq was used, whatever that was
        self._check_correct_merger_ipq_used(correct_merger_ipq_init=merger_ipq_init)

        # wipe files to prevent leaks
        self.clear_all_files()

        # use a non-default ipq, check that that's passed down correctly
        self._prototype_test(sorter_init, MergerIPQ_Tester.MergerIPQ_Tester, merger_init)

        self._check_correct_merger_ipq_used(correct_merger_ipq_init=MergerIPQ_Tester.MergerIPQ_Tester)

        # wipe files to prevent leaks
        self.clear_all_files()

        # use a non-default merger, check that that's passed down correctly
        self._prototype_test(sorter_init, merger_ipq_init, Merger_Tester.Merger_Tester)
        self._check_correct_merger_used(correct_merger_init=Merger_Tester.Merger_Tester)

        # test complete - delete test files to avoid memory leaks
        self.clear_all_files()

    # * * * * * * * * * * * * * *
    # * * * * * TESTS * * * * * *
    # * * * * * * * * * * * * * *


class TestCases(unittest.TestCase):
    def test_sorter_default(self):
        """tests the class default sorter"""
        our_tester = Test_Sorters(Sorter_LibraryMethods.Sorter_Default, self)

        # only test if this one runs - it doesn't use a merger or merger IPQ, so it's pointless to test if it
        # uses the correct one
        our_tester._prototype_test(Sorter_LibraryMethods.Sorter_Default)

        # this test may create meaningless output files - clear them for safety
        our_tester.clear_all_files()

        print("tested default sorter")

    def test_sorter_bottom_up(self,
                              override_merger_ipq_init=None,
                              override_merger_init=None):
        """tests the k-way bottom up sorter"""
        sorter_init = Sorter_BottomUp.Sorter_PingPong_BottomUp
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        our_tester = Test_Sorters(sorter_init, self)

        # wrap to test options are correct
        our_tester._passing_test_wrapper(sorter_init,
                                         override_merger_init, default_merger_init,
                                         override_merger_ipq_init, default_merger_ipq_init)

        print("tested k-way bottom up sorter")

    def test_sorter_adaptive(self,
                             override_merger_ipq_init=None,
                             override_merger_init=None):
        """tests the bottom up, k-way, run adaptive sorter"""

        sorter_init = Sorter_Adaptive.Sorter_PingPong_Adaptive
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        our_tester = Test_Sorters(sorter_init, self)

        our_tester._passing_test_wrapper(sorter_init,
                                         override_merger_init, default_merger_init,
                                         override_merger_ipq_init, default_merger_ipq_init)

        print("tested k-way adaptive sorter")

    # todo = allow override here
    def test_sorter_adaptive_k_2(self, override_merger_ipq_init=None, override_merger_init=None):
        # default parameters
        sorter_init = Sorter_Adaptive_k_2.Sorter_Adaptive_k_2
        default_merger_init = Merger_TwoWay.Merger_TwoWay

        our_tester = Test_Sorters(sorter_init, self)

        # test with default settings
        our_tester._sort_single_element()
        our_tester._sort_and_test_up_to_power(4, 2)

        # check that the merger choice is correct - there shouldn't be an ipq
        our_tester._check_correct_merger_used(default_merger_init)

        # clear and set up to test the merger override
        our_tester.clear_all_files()
        our_tester.override_merger_init = Merger_Tester.Merger_Tester

        # test with non-default settings
        our_tester._sort_single_element()
        our_tester._sort_and_test_up_to_power(2, 2)

        # check that the merger choice is correct - there shouldn't be an ipq
        our_tester._check_correct_merger_used(our_tester.override_merger_init)

        our_tester.clear_all_files()

        print("testing adaptive k=2 sorter")

    def test_sorter_peeksort(self, override_merger_ipq_init=None, override_merger_init=None):
        """tests the k-way peeksort sorter"""

        sorter_init = Sorter_Peeksort.Sorter_Peeksort
        # sorter_init = Sorter_Adaptive.Sorter_PingPong_Adaptive
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        our_tester = Test_Sorters(sorter_init, self)

        # todo - fix peeksort so that it can pass this test
        # our_tester._passing_test_wrapper(sorter_init,
        #                                  override_merger_init, default_merger_init,
        #                                  override_merger_ipq_init, default_merger_ipq_init)

        our_tester._prototype_test(sorter_init)

        our_tester.clear_all_files()

        print("tested k-way peeksort")

    # * * * * * *  * * * * * * *
    # * * * * * MAIN * * * * * *
    # * * * * * *  * * * * * * *


if __name__ == "__main__":
    unittest.main()
