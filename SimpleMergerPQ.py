import MergerIPQ


class SimpleMergerPQ(MergerIPQ.MergerIPQ):
    def __init__(self, initial_priorities):
        self.priorities = initial_priorities.copy()

    def build_index_priority_queue(self, initial_priorities: list) -> None:
        pass

    def get_name(self):
        return self.__class__.__name__

    def update_lowest_priority(self, new_priority: int) -> None:
        """

        :type new_priority: int
        """
        min_priority_index = self.peek_at_lowest_priority_element()[0]

        self.priorities[min_priority_index] = new_priority

    def peek_at_lowest_priority_element(self) -> (int, int):
        min_priority_run = 0
        min_priority_value = self.priorities[0]

        for i in range(len(self.priorities)):
            # confusion here - index is in the external array,
            # we should really be looking at which run is the min
            # for the purpose of line 30

            if self.priorities[i] < min_priority_value:
                min_priority_run = i
                min_priority_value = self.priorities[i]

        return [min_priority_run, min_priority_value]
