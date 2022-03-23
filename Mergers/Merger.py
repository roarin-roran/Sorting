from typing import List
from Support import ListSlice
from Merger_IPQs import MergerIPQ_Dummy
from os.path import exists


class Merger:
    def __init__(self, runs: List[ListSlice.ListSlice], write_list_slice: ListSlice.ListSlice, option_code: int,
                 merger_ipq_init=False,
                 test_mode=False) -> None:
        """records the input and performs setup tasks

        input will be a list of ListSlice objects, which each point to a list, and have start and end indices in that
        list
        """
        self.runs = runs
        self.write_list_slice = write_list_slice

        # if no merger_ipq_init is passed, use a default
        if merger_ipq_init:
            self.merger_ipq_init = merger_ipq_init
        else:
            self.merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        self.option_code = option_code
        self.test_mode = test_mode

        if test_mode:
            self.record_options(option_code)

    def merge(self) -> ListSlice.ListSlice:
        """merges the elements passed at object creation by modifying the original list, returning a ListSlice with the
        new run"""
        raise NotImplementedError("merge is not implemented")

    @staticmethod
    def record_options(option_code):
        """records which merger is used to an external file for testing purposes"""

        num_options = 0
        # only write unique inputs
        if exists("test_options_merger.txt"):
            f_r = open("test_options_merger.txt", "r")
            for entry in f_r:
                if entry == str(option_code) + "\n":
                    return
                else:
                    num_options += 1
            f_r.close()

        if num_options > 0:
            raise ValueError("multiple mergers used in the same test - not currently supported")

        f_a = open("test_options_merger.txt", "a")

        f_a.write(str(option_code))
        f_a.write("\n")
        f_a.close()
