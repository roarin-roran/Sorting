# a trimmed down version of a priority queue for use in merge sorting algorithms
from typing import Type, TypeVar, List, Tuple

# define the type of the priorities we're using
PRIORITY_TYPE = TypeVar('PRIORITY_TYPE')


class MergerIPQ:
    # do we really need this?
    def build_index_priority_queue(self, initial_priorities: List[PRIORITY_TYPE]) -> None:
        """FORMALISE: input initial_priorities has priorities according to index. index == run ID

        pair = (i, initialPriorities[i])

        Builds the IPQ, partially sorting the input array (details differ in different implementations)"""
        pass

    def update_lowest_priority(self, new_priority: PRIORITY_TYPE) -> None:
        """Updates the priority of the lowest priority element"""
        pass

    def peek_at_lowest_priority_element(self) -> Tuple[int, PRIORITY_TYPE]:
        """returns the index of the highest priority element, without modifying it"""
        pass
    def peek_at_lowest_priority_element2(self) -> (int, PRIORITY_TYPE):
        """returns the [index,priority] of the lowest priority element, without modifying it"""
        pass
