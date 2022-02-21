import SimpleMergerPQ


def test_simple_merger():
    sample_input = [4, 3, 2, 1]

    our_simple_merger = SimpleMergerPQ.SimpleMergerPQ(sample_input)

    print(our_simple_merger.peek_at_lowest_priority_element())

    our_simple_merger.update_lowest_priority(17)

    print(our_simple_merger.peek_at_lowest_priority_element())


test_simple_merger()
