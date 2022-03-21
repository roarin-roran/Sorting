from typing import List
from Support import ListSlice
from Merger_IPQs import MergerIPQ_Dummy


class Merger:
    def __init__(self, runs: List[ListSlice.ListSlice], write_list_slice: ListSlice.ListSlice,
                 merger_ipq_init=False) -> None:
        """records the input and performs setup tasks

        input will be a list of ListSlice objects, which each point to a list, and have start and end indices in that
        list
        """
        self.runs = runs
        self.write_list_slice = write_list_slice
        if merger_ipq_init:
            self.merger_ipq_init = merger_ipq_init
        else:
            self.merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

    def merge(self) -> ListSlice.ListSlice:
        """merges the elements passed at object creation by modifying the original list, returning a ListSlice with the
        new run"""
        raise NotImplementedError("merge is not implemented")
