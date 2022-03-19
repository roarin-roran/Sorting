from typing import List
import ListSlice


class Merger:
    def __init__(self, runs: List[ListSlice.ListSlice], write_list: ListSlice.ListSlice) -> None:
        """records the input and performs setup tasks

        input will be a list of ListSlice objects, which each point to a list, and have start and end indices in that
        list
        """

        pass


    def merge(self) -> ListSlice.ListSlice:
        """merges the elements passed at object creation by modifying the original list, returning a ListSlice with the
        new run"""

        print("merge is not implemented")
        raise NotImplementedError
