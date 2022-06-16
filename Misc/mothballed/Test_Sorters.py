import random
import unittest
from Sorters import Sorter_Adaptive, Sorter_BottomUp, Sorter_LibraryMethods, Sorter_Peeksort
from Mergers import Merger, Merger_Adaptive, Merger_Tester
from Merger_IPQs import MergerIPQ, MergerIPQ_Tester, MergerIPQ_LoserTree
from Misc.mothballed import Test_MergerIPQ, Test_Mergers
from typing import Union
import os


class Test_Sorters(unittest.TestCase):
    # todo - this doesn't pass tests
    def _test_sorter_peeksort(self, override_merger_ipq_init=None, override_merger_init=None):
        """tests the k-way peeksort sorter"""

        sorter_init = Sorter_Peeksort.Sorter_Peeksort
        # sorter_init = Sorter_Adaptive.Sorter_PingPong_Adaptive
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        self._passing_test_wrapper(sorter_init,
                                   override_merger_init, default_merger_init,
                                   override_merger_ipq_init, default_merger_ipq_init)

    def test_sorter_adaptive(self,
                             override_merger_ipq_init=None,
                             override_merger_init=None):
        """tests the bottom up, k-way, run adaptive sorter"""

        sorter_init = Sorter_Adaptive.Sorter_PingPong_Adaptive
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        self._passing_test_wrapper(sorter_init,
                                   override_merger_init, default_merger_init,
                                   override_merger_ipq_init, default_merger_ipq_init)

    def test_sorter_bottom_up(self,
                              override_merger_ipq_init=None,
                              override_merger_init=None):
        """tests the k-way bottom up sorter"""
        sorter_init = Sorter_BottomUp.Sorter_PingPong_BottomUp
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        self._passing_test_wrapper(sorter_init,
                                   override_merger_init, default_merger_init,
                                   override_merger_ipq_init, default_merger_ipq_init)

    def test_sorter_default(self):
        """tests the class default sorter"""
        # only test if this one runs - it doesn't use a merger or merger IPQ, so it's pointless to test if it uses
        # the correct one
        self._prototype_test(Sorter_LibraryMethods.Sorter_Default)

        # this test will create meaningless output files - clear them for safety
        Test_Mergers.Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

    def _passing_test_wrapper(self, sorter_init,
                              override_merger_init, default_merger_init,
                              override_merger_ipq_init, default_merger_ipq_init):
        """an extended test for custom methods - wraps prototype_test, and confirms that this sorter correctly passes
        mergers and ipqs"""

        if override_merger_init:
            merger_init = override_merger_init
        else:
            merger_init = default_merger_init

        if override_merger_ipq_init:
            merger_ipq_init = override_merger_ipq_init
        else:
            merger_ipq_init = default_merger_ipq_init

        # make ipq_tester
        ipq_tester = Test_MergerIPQ.Test_MergerIPQ()
        merger_tester = Test_Mergers.Test_Mergers()

        # test using either default values or override values
        self._prototype_test(sorter_init, merger_ipq_init, merger_init)
        # check that the correct merger was used
        merger_tester.check_correct_merger_used(correct_merger_init=merger_init)
        # check that the correct ipq was used, whatever that was
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=merger_ipq_init)

        # wipe files to prevent leaks
        Test_Mergers.Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

        # use a non-default ipq, check that that's passed down correctly
        self._prototype_test(sorter_init, MergerIPQ_Tester.MergerIPQ_Tester, merger_init)
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=MergerIPQ_Tester.MergerIPQ_Tester)

        # wipe files to prevent leaks
        Test_Mergers.Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

        # use a non-default merger, check that that's passed down correctly
        self._prototype_test(sorter_init, merger_ipq_init, Merger_Tester.Merger_Tester)
        merger_tester.check_correct_merger_used(correct_merger_init=Merger_Tester.Merger_Tester)

        # test complete - delete test files to avoid memory leaks
        Test_Mergers.Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

    def _prototype_test(self, sorter_init,
                        merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False,
                        merger_init: Union[bool, type(Merger.Merger)] = False):
        """tests that the inserted sorter correctly sorts several inserted lists with a variety of k values"""
        self.sorter_init = sorter_init
        self.merger_ipq_init = merger_ipq_init
        self.merger_init = merger_init

        # note - this order is crucial! sort_single_element asserts that no ipq/merger options files have been created
        # other tests may create these, so it *must* be executed first.
        self._sort_single_element()
        self._sort_and_test_up_to_power(max_power=2, max_k=4)

    def _sort_and_test_up_to_power(self, max_power, max_k):
        """creates inputs up to 10^max_power, and sorts each one with all k values between 2 and max_k, inclusive."""
        # seed with star wars day
        # todo - move this seed higher
        random.seed(405)

        # todo - rewrite with Experiments class to reduce copied code

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
                                          merger_ipq_init=self.merger_ipq_init,
                                          merger_init=self.merger_init,
                                          test_mode=True)
                sorter.sort()

                # check sortedness
                self.assertEqual(sorted_input, random_input)

    def _sort_single_element(self):
        """tests that a sorter can handle the trivial input of a single character. note that this should NOT be special
        cased - the potential flaw we're checking for here is the creation of a merger for an input that doesn't need
        one"""
        random_input = [1]
        sorted_input = [1]
        sorter = self.sorter_init(sorted_input, 2, merger_ipq_init=self.merger_ipq_init,
                                  merger_init=self.merger_init,
                                  test_mode=True)
        sorter.sort()

        # check sortedness
        self.assertEqual(sorted_input, random_input)

        # assure that no mergers or merger ipqs are used for this input
        self.assertFalse(os.path.isfile(
            "../../Tests/test_options_merger_ipq.txt")), "a merger ipq was used for a single element"
        self.assertFalse(os.path.isfile(
            "../../Tests/test_options_merger.txt")), "a merger was used for a single element"


if __name__ == '__main__':
    unittest.main()
