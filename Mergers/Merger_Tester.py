from Mergers import Merger_Adaptive
from Support import ListSlice
from typing import List


class Merger_Tester(Merger_Adaptive.Merger_Adaptive):
    """a reskin of the adaptive merger used to test whether variables are passed correctly"""
    def __init__(self, runs: List[ListSlice.ListSlice],
                 write_list_slice: ListSlice.ListSlice,
                 option_code=0,
                 merger_ipq_init=False,
                 test_mode=True):
        super().__init__(runs, write_list_slice,
                         option_code,
                         merger_ipq_init,
                         test_mode=test_mode)
