import unittest
from Tests import Test_Sorters
from Merger_IPQs import MergerIPQ_Dummy


class Test_MergerIPQ(unittest.TestCase):

    def test_dummy_ipq(self):
        self.prototype_test(MergerIPQ_Dummy.MergerIPQ_Dummy)

    def prototype_test(self, merger_ipq_init):
        self.fixed_tests(merger_ipq_init)

        sorter_tester = Test_Sorters.Test_Sorters()
        sorter_tester.test_sorter_bottom_up(merger_ipq_init=merger_ipq_init)

    def fixed_tests(self, init_merger_ipq):
        sample_input = [4, 3, 2, 1]

        our_simple_merger = init_merger_ipq(sample_input)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (3, 1))

        our_simple_merger.update_lowest_priority(17)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (2, 2))

        our_simple_merger.update_lowest_priority(12)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (1, 3))

        our_simple_merger.update_lowest_priority(15)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (0, 4))

        our_simple_merger.update_lowest_priority(34)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (2, 12))
