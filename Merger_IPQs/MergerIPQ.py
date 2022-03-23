# a trimmed down version of a priority queue for use in merge sorting algorithms
from typing import TypeVar, List, Tuple
from os.path import exists

# define the type of the priorities we're using
PRIORITY_TYPE = TypeVar('PRIORITY_TYPE')


class MergerIPQ:
    def __init__(self, initial_priorities: List[PRIORITY_TYPE], option_code: int,
                 test_mode=False) -> None:
        """FORMALISE: input initial_priorities has priorities according to index. index == run ID

        pair = (i, initialPriorities[i])

        Builds the IPQ, partially sorting the input array (details differ in different implementations)"""
        self.priorities = initial_priorities
        self.option_code = option_code
        self.test_mode = test_mode

        if test_mode:
            self.record_options(option_code)

    def update_lowest_priority(self, new_priority: PRIORITY_TYPE) -> None:
        """Updates the priority of the lowest priority element"""
        raise NotImplementedError("update_lowest_priority is not implemented")

    def peek_at_lowest_priority_element(self) -> Tuple[int, PRIORITY_TYPE]:
        """returns the index of the highest priority element, without modifying it"""
        raise NotImplementedError("peek_at_lowest_priority_element is not implemented")

    @staticmethod
    def record_options(option_code):
        """records which IPQ is used to an external file for testing purposes"""
        if exists("test_options_merger_ipq.txt"):
            f_r = open("test_options_merger_ipq.txt", "r")
            for entry in f_r:
                if entry == str(option_code)+"\n":
                    return
            f_r.close()

        f_a = open("test_options_merger_ipq.txt", "a")

        f_a.write(str(option_code))
        f_a.write("\n")
        f_a.close()
