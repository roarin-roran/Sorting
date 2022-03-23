import random
import unittest
from Sorters import Sorter_Adaptive, Sorter_BottomUp, Sorter_LibraryMethods
from Mergers import Merger, Merger_Adaptive, Merger_Tester
from Merger_IPQs import MergerIPQ, MergerIPQ_Dummy, MergerIPQ_Tester
from Tests import Test_MergerIPQ, Test_Mergers
from typing import Union


class Test_Sorters(unittest.TestCase):
    def test_sorter_adaptive(self,
                             override_merger_ipq_init=False,
                             override_merger_init=False):
        sorter_init = Sorter_Adaptive.Sorter_PingPong_Adaptive
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        self.passing_test_wrapper(sorter_init,
                                  override_merger_init, default_merger_init,
                                  override_merger_ipq_init, default_merger_ipq_init)

    def test_sorter_bottom_up(self,
                              override_merger_ipq_init=False,
                              override_merger_init=False):
        sorter_init = Sorter_BottomUp.Sorter_PingPong_BottomUp
        default_merger_init = Merger_Adaptive.Merger_Adaptive
        default_merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        self.passing_test_wrapper(sorter_init,
                                  override_merger_init, default_merger_init,
                                  override_merger_ipq_init, default_merger_ipq_init)

    def test_sorter_default(self):
        # only test if this one runs - it doesn't use a merger or merger IPQ, so it's pointless to test if it uses
        # the correct one
        self.prototype_test(Sorter_LibraryMethods.Sorter_Default)

    def passing_test_wrapper(self, sorter_init,
                             override_merger_init, default_merger_init,
                             override_merger_ipq_init, default_merger_ipq_init):

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
        self.prototype_test(sorter_init, merger_ipq_init, merger_init)
        # check that the correct merger was used
        merger_tester.check_correct_merger_used(correct_merger_init=merger_init)
        # check that the correct ipq was used, whatever that was
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=merger_ipq_init)

        # use a non-default ipq, check that that's passed down correctly
        self.prototype_test(sorter_init, MergerIPQ_Tester.MergerIPQ_Tester, merger_init)
        ipq_tester.check_correct_merger_ipq_used(correct_merger_ipq_init=MergerIPQ_Tester.MergerIPQ_Tester)

        # use a non-default merger, check that that's passed down correctly
        self.prototype_test(sorter_init, merger_ipq_init, Merger_Tester.Merger_Tester)
        # os.remove("test_options_merger.txt")

        # os.remove("test_options_merger_ipq.txt")
        merger_tester.check_correct_merger_used(correct_merger_init=Merger_Tester.Merger_Tester)

    def prototype_test(self, sorter_init,
                       merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False,
                       merger_init: Union[bool, type(Merger.Merger)] = False):
        self.sorter_init = sorter_init
        self.merger_ipq_init = merger_ipq_init
        self.merger_init = merger_init

        Test_Mergers.Test_Mergers.clear_file_merger()
        Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

        self.sort_and_test_up_to_power(3)

    def sort_and_test_up_to_power(self, max_power):
        for power in range(1, max_power):
            self.sort_n_inputs(n=10**power)

    def sort_n_inputs(self, n):
        random.seed(n)

        random_input = list(range(n))
        sorted_input = random_input.copy()

        for k in range(2, 5):
            random.shuffle(random_input)

            sorter = self.sorter_init(random_input, k,
                                      merger_ipq_init=self.merger_ipq_init,
                                      merger_init=self.merger_init,
                                      test_mode=True)
            sorter.sort()

            self.assertEqual(random_input, sorted_input)


if __name__ == '__main__':
    unittest.main()
