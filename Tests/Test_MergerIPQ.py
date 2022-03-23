import unittest
from Tests import Test_Sorters
from Merger_IPQs import MergerIPQ_Dummy, MergerIPQ_Tester
import os
from os.path import exists


class Test_MergerIPQ(unittest.TestCase):

    def test_tests(self):
        """ensures that the tests below correctly use the desired ipq"""
        self.prototype_test(MergerIPQ_Tester.MergerIPQ_Tester)

    def test_dummy_ipq(self):
        self.prototype_test(MergerIPQ_Dummy.MergerIPQ_Dummy)

    def prototype_test(self, merger_ipq_init):
        """a prototype for all testing of merger ipqs - call it with the right init and let her rip"""
        # use the ipq at issue to do a sorting test - high volume random values, testing for problems caused by the ipq
        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(override_merger_ipq_init=merger_ipq_init)

        # apply fixed tests - use human generated values to reproduce expected behaviour
        self.fixed_tests(merger_ipq_init)
        # check that the desired merger_ipq was used and no other merger_ipq was used
        self.check_correct_merger_ipq_used(merger_ipq_init)

    def fixed_tests(self, merger_ipq_init):
        sample_input = [4, 3, 2, 1]

        our_simple_merger = merger_ipq_init(sample_input, test_mode=True)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (3, 1))

        our_simple_merger.update_lowest_priority(17)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (2, 2))

        our_simple_merger.update_lowest_priority(12)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (1, 3))

        our_simple_merger.update_lowest_priority(15)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (0, 4))

        our_simple_merger.update_lowest_priority(34)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (2, 12))

    def check_correct_merger_ipq_used(self, correct_merger_ipq_init):
        blank_merger_ipq = correct_merger_ipq_init([])
        f_r = open("test_options_merger_ipq.txt", "r")

        correct_answer = str(blank_merger_ipq.option_code)

        for entry in f_r:
            given_answer = entry[0]
            self.assertEqual(correct_answer, given_answer)

        f_r.close()

        # remove the test options file - calling this function implies a complete test has finished
        os.remove("test_options_merger_ipq.txt")

    @staticmethod
    def print_options_merger_ipq():
        if exists("test_options_merger_ipq.txt"):
            f_r = open("test_options_merger_ipq.txt", "r")
            for entry in f_r:
                print(entry)
