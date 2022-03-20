import unittest
import MergerIPQ_Dummy


class Test_MergerIPQ(unittest.TestCase):

    def test_dummy_ipq(self):
        sample_input = [4, 3, 2, 1]

        our_simple_merger = MergerIPQ_Dummy.MergerIPQ_Dummy(sample_input)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (3, 1))

        our_simple_merger.update_lowest_priority(17)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (2, 2))

        our_simple_merger.update_lowest_priority(12)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (1, 3))

        our_simple_merger.update_lowest_priority(15)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (0, 4))

        our_simple_merger.update_lowest_priority(34)

        self.assertEqual(our_simple_merger.peek_at_lowest_priority_element(), (2, 12))






