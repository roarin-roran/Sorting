from typing import List
from Support import ListSlice
from Merger_IPQs import MergerIPQ_LoserTree
from os.path import exists


class Merger:
    """accepts a list of list slices to merge and a list slice to write to - uses merge method to merge the input
    into the output """
    def __init__(self, runs: List[ListSlice.ListSlice], write_list_slice: ListSlice.ListSlice, option_code,
                 merger_ipq_init=False,
                 test_mode=False) -> None:
        self.runs = runs
        self.write_list_slice = write_list_slice
        self.option_code = option_code

        # if no merger_ipq_init is passed, use a default
        if merger_ipq_init:
            self.merger_ipq_init = merger_ipq_init
        else:
            self.merger_ipq_init = MergerIPQ_LoserTree.MergerIPQ_LoserTree

        self.test_mode = test_mode

        if test_mode:
            self.record_options()

    def merge(self) -> ListSlice.ListSlice:
        """merges the elements passed at object creation by modifying the original list, modifying the write slice"""
        raise NotImplementedError("merge is not implemented")

    def record_options(self):
        """records which merger is used to an external file for testing purposes"""
        num_options = 0
        # only write unique inputs
        if exists("test_options_merger.txt"):
            f_r = open("test_options_merger.txt", "r")
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

        f_a = open("test_options_merger.txt", "a")

        f_a.write(str(self.option_code.value))
        f_a.write("\n")
        f_a.close()
