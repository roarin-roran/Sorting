from Mergers import Merger_Adaptive
from Support import ListSlice
from typing import List
from Codes import Code_Merger


class Merger_Tester(Merger_Adaptive.Merger_Adaptive):
    """a re-skin of the adaptive merger used to test whether variables are passed correctly"""
    def __init__(self, runs: List[ListSlice.ListSlice], write_list_slice: ListSlice.ListSlice,
                 merger_ipq_init=False, test_mode=True):
        super().__init__(runs, write_list_slice, merger_ipq_init,
                         test_mode=test_mode,
                         option_code=Code_Merger.Code_Merger.TESTER)

