# a trimmed down version of a priority queue for use in merge sorting algorithms
from typing import TypeVar, List, Tuple
from os.path import exists

# define the type of the priorities we're using
PRIORITY_TYPE = TypeVar('PRIORITY_TYPE')


class MergerIPQ:
    def __init__(self, initial_priorities: List[PRIORITY_TYPE], option_code: int, test_mode=False) -> None:
        """an informal interface for an indexed priority queue, with a few shared helper methods built in"""
        self.priorities = initial_priorities
        self.option_code = option_code

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

        num_options = 0

        if exists("test_options_merger_ipq.txt"):
            f_r = open("test_options_merger_ipq.txt", "r")
            for entry in f_r:
                if entry == str(option_code)+"\n":
                    return
                else:
                    num_options += 1
            f_r.close()

        if num_options > 0:
            raise ValueError("multiple ipqs used in the same test - not currently supported:", option_code, "not added")

        f_a = open("test_options_merger_ipq.txt", "a")

        f_a.write(str(option_code))
        f_a.write("\n")
        f_a.close()
