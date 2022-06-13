from Tests import Test, Test_Sorters
from Merger_IPQs import MergerIPQ_Tester, MergerIPQ_Dummy, MergerIPQ_LoserTree
import unittest


class Test_MergerIPQs(Test.Test):
    def __init__(self, merger_ipq_init, test_case, check_ipq_selection=False, check_merger_selection=False):
        super().__init__(check_ipq_selection, check_merger_selection)

        self.test_case = test_case

        self.merger_ipq_init = merger_ipq_init

    # * * * * * * * * * * * * * *
    # * * * * * UTILITY * * * * *
    # * * * * * * * * * * * * * *

    def _prototype_test(self):
        """a prototype for all testing of merger ipqs - call it with the right init and let her rip"""
        # clear files to prevent memory leaks
        self.clear_unnecessary_files()

        # ensure that a test failing to run doesn't leak
        test_completed = False
        try:
            # 1. use the ipq at issue to do a sorting test:
            #    high volume random values, testing for problems caused by this ipq
            sorter_tester = Test_Sorters.Test_Sorters()
            sorter_tester.test_sorter_bottom_up(override_merger_ipq_init=self.merger_ipq_init)

            # 2. apply fixed tests - use human generated values to reproduce expected behaviour
            self._fixed_tests(self.merger_ipq_init)

            # 3. check that the desired merger_ipq was used and no other merger_ipq was used
            self._check_correct_merger_ipq_used(self.merger_ipq_init)

            test_completed = True
        finally:
            if not test_completed:
                self.test_case.fail(msg="ipq test failed to complete")

        # clear files to prevent memory leaks
        self.clear_unnecessary_files()

    def _fixed_tests(self, merger_ipq_init):
        """test the ipq with fixed, well defined values - covering all core methods"""
        sample_input = [4, 3, 2, 1]

        our_simple_merger = merger_ipq_init(sample_input, test_mode=True)

        self.test_case.assertEqual((3, 1), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(17)

        self.test_case.assertEqual((2, 2), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(12)

        self.test_case.assertEqual((1, 3), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(15)

        self.test_case.assertEqual((0, 4), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(34)

        self.test_case.assertEqual((2, 12), our_simple_merger.peek_at_lowest_priority_element())

    # * * * * * * * * * * * * * *
    # * * * * * TESTS * * * * * *
    # * * * * * * * * * * * * * *


class TestCases(unittest.TestCase):

    def test_tests(self):
        """ensures that the tests below correctly use the desired ipq"""
        our_tester = Test_MergerIPQs(MergerIPQ_Tester.MergerIPQ_Tester, self)
        our_tester._prototype_test()

        print("tested ipq tests")

    def test_dummy_ipq(self):
        """tests the simple ipq"""
        our_tester = Test_MergerIPQs(MergerIPQ_Dummy.MergerIPQ_Dummy, self)
        our_tester._prototype_test()

        print("tested dummy ipq")

    def test_loser_tree_ipq(self):
        """tests the loser tree based ipq"""
        our_tester = Test_MergerIPQs(MergerIPQ_LoserTree.MergerIPQ_LoserTree, self)
        our_tester._prototype_test()

        print("tested loser tree ipq")

    # * * * * * *  * * * * * * *
    # * * * * * MAIN * * * * * *
    # * * * * * *  * * * * * * *


if __name__ == "__main__":
    unittest.main()
