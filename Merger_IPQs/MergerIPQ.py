# a trimmed down version of a priority queue for use in merge sorting algorithms
from typing import TypeVar, List, Tuple

# define the type of the priorities we're using
PRIORITY_TYPE = TypeVar('PRIORITY_TYPE')


class MergerIPQ:
    def __init__(self, initial_priorities: List[PRIORITY_TYPE]) -> None:
        """FORMALISE: input initial_priorities has priorities according to index. index == run ID

        pair = (i, initialPriorities[i])

        Builds the IPQ, partially sorting the input array (details differ in different implementations)"""
        self.priorities = initial_priorities

    def update_lowest_priority(self, new_priority: PRIORITY_TYPE) -> None:
        """Updates the priority of the lowest priority element"""
        raise NotImplementedError("update_lowest_priority is not implemented")

    def peek_at_lowest_priority_element(self) -> Tuple[int, PRIORITY_TYPE]:
        """returns the index of the highest priority element, without modifying it"""
        raise NotImplementedError("peek_at_lowest_priority_element is not implemented")
