# a trimmed down version of a priority queue for use in merge sorting algorithms
from typing import Type

# define the type of the priorities we're using
# (kinda sketch.. but ultimately we're unlikely to need to use non-ints here)
# noinspection PyTypeChecker
PRIORITY_TYPE: Type[Type] = int


class MergerIPQ:
    # do we really need this?
    def build_index_priority_queue(self, initial_priorities: list) -> None:
        """FORMALISE: input initial_priorities has priorities according to index. index == run ID

        pair = (i, initialPriorities[i])

        Builds the IPQ, partially sorting the input array (details differ in different implementations)"""
        pass

    def update_lowest_priority(self, new_priority: PRIORITY_TYPE) -> None:
        """Updates the priority of the lowest priority element"""
        pass

    def peek_at_lowest_priority_element(self) -> [int, int]:
        """returns the [index,priority] of the lowest priority element, without modifying it"""
        pass
