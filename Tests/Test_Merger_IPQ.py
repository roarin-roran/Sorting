from Tests import Test, Test_Sorters
from Merger_IPQs import MergerIPQ_Tester, MergerIPQ_Dummy, MergerIPQ_LoserTree
import unittest


class Test_MergerIPQ(Test.Test):
    def __init__(self, merger_ipq_init,
                 check_ipq_selection=False,
                 check_merger_selection=False):
        super().__init__(check_ipq_selection, check_merger_selection)

        self.merger_ipq_init = merger_ipq_init

    def _prototype_test(self):
        """a prototype for all testing of merger ipqs - call it with the right init and let her rip"""
        # clear files to prevent memory leaks
        self.clear_unnecessary_files()

        # 1. use the ipq at issue to do a sorting test:
        #    high volume random values, testing for problems caused by this ipq
        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(override_merger_ipq_init=self.merger_ipq_init)

        # 2. apply fixed tests - use human generated values to reproduce expected behaviour
        self._fixed_tests(self.merger_ipq_init)

        # 3. check that the desired merger_ipq was used and no other merger_ipq was used
        self.check_correct_merger_ipq_used(self.merger_ipq_init)

        # clear files to prevent memory leaks
        self.clear_unnecessary_files()

    def _fixed_tests(self, merger_ipq_init):
        """test the ipq with fixed, well defined values - covering all core methods"""
        sample_input = [4, 3, 2, 1]

        our_simple_merger = merger_ipq_init(sample_input, test_mode=True)

        self.assertEqual((3, 1), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(17)

        self.assertEqual((2, 2), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(12)

        self.assertEqual((1, 3), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(15)

        self.assertEqual((0, 4), our_simple_merger.peek_at_lowest_priority_element())

        our_simple_merger.update_lowest_priority(34)

        self.assertEqual((2, 12), our_simple_merger.peek_at_lowest_priority_element())

    def check_correct_merger_ipq_used(self, correct_merger_ipq_init):
        """checks that the input is the only ipq used since records were last wiped"""
        blank_merger_ipq = correct_merger_ipq_init([])
        f_r = open("test_options_merger_ipq.txt", "r")

        correct_answer = str(blank_merger_ipq.option_code)

        for entry in f_r:
            given_answer = entry[0]
            self.assertEqual(correct_answer, given_answer)

        f_r.close()

    def test_tests(self):
        """ensures that the tests below correctly use the desired ipq"""
        our_tester = Test_MergerIPQ(MergerIPQ_Tester.MergerIPQ_Tester)
        our_tester._prototype_test()

        print("test 1")

    def test_dummy_ipq(self):
        """tests the simple ipq"""
        our_tester = Test_MergerIPQ(MergerIPQ_Dummy.MergerIPQ_Dummy)
        our_tester._prototype_test()

        print("test 2")

    def test_tournament_ipq(self):
        """tests the tournament tree based ipq"""
        our_tester = Test_MergerIPQ(MergerIPQ_LoserTree.MergerIPQ_LoserTree)
        our_tester._prototype_test()

        print("test 3")

    # todo - why is this even necessary? if a test isn't copied in here, it says that it runs... but doesn't
    def runTest(self):
        self.test_tests()
        self.test_dummy_ipq()
        self.test_tournament_ipq()


if __name__ == "__main__":
    unittest.main()
