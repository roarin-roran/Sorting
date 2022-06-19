# a trimmed down version of a priority queue for use in merge sorting algorithms
from typing import TypeVar, List, Tuple
from os.path import exists
from Codes import Code_Merger


# define the type of the priorities we're using
PRIORITY_TYPE = TypeVar('PRIORITY_TYPE')


class MergerIPQ:
    def __init__(self, initial_priorities: List[PRIORITY_TYPE],
                 option_code=Code_Merger.Code_Merger.BASE,
                 test_mode=False) -> None:
        """an informal interface for an indexed priority queue, with a few shared helper methods built in"""

        self.option_code = option_code

        if test_mode:
            self.record_options()

    def update_lowest_priority(self, new_priority: PRIORITY_TYPE) -> None:
        """Updates the priority of the lowest priority element"""
        raise NotImplementedError("update_lowest_priority is not implemented")

    def peek_at_lowest_priority_element(self) -> Tuple[int, PRIORITY_TYPE]:
        """returns the index of the highest priority element, without modifying it"""
        raise NotImplementedError("peek_at_lowest_priority_element is not implemented")

    def record_options(self):
        """records which merger IPQ is used to an external file for testing purposes"""
        num_options = 0
        # only write unique inputs
        if exists("test_options_merger_ipq.txt"):
            f_r = open("test_options_merger_ipq.txt", "r")
            all_options = [str(self.option_code.value)]
            for entry in f_r:
                all_options.append(entry[0])

                if entry == str(self.option_code.value) + "\n":
                    f_r.close()
                    return
                else:
                    num_options += 1
            f_r.close()

            if num_options > 0:
                raise ValueError("multiple mergers used in the same test - not currently supported. options used:",
                                 all_options)

        f_a = open("test_options_merger_ipq.txt", "a")

        f_a.write(str(self.option_code.value))
        f_a.write("\n")
        f_a.close()
