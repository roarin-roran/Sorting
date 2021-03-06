from Merger_IPQs import MergerIPQ
from Codes import Code_IPQ


class MergerIPQ_Dummy(MergerIPQ.MergerIPQ):
    """a simple dummy method for IPQ implementations - methods work, but are far from optimised"""

    # add an additional input to be used exclusively by tester
    def __init__(self, initial_priorities, test_mode=False, option_code=Code_IPQ.Code_Ipq.DUMMY):
        super().__init__(initial_priorities, option_code, test_mode)
        self.priorities = initial_priorities

    def update_lowest_priority(self, new_priority: int) -> None:
        """Updates the priority of the lowest priority element"""
        min_priority_index = self.peek_at_lowest_priority_element()[0]

        self.priorities[min_priority_index] = new_priority

    def peek_at_lowest_priority_element(self) -> (int, int):
        """returns the (index, value) of the highest priority element, without modifying it"""
        min_priority_run = 0
        min_priority_value = self.priorities[0]

        for i in range(len(self.priorities)):
            # confusion here - index is in the external array,
            # we should really be looking at which run is the min
            # for the purpose of line 30

            if self.priorities[i] < min_priority_value:
                min_priority_run = i
                min_priority_value = self.priorities[i]

        return min_priority_run, min_priority_value
