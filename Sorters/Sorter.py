# notes:
# 1. at some point, "day trip" array management will be used in place of ping pong, for methods like powersort
#   which lack clear run definitions
from Mergers import Merger_Adaptive


class Sorter:
    """an informal interface for sorters, which accept a list as input, then sort that list in various ways"""
    def __init__(self, input_list,
                 k=2,
                 merger_ipq_init=None,
                 merger_init=None,
                 test_mode=False):
        self.input_list = input_list
        self.k = k
        self.merger_ipq_init = merger_ipq_init

        # if no merger is selected, use a default
        if merger_init:
            self.merger_init = merger_init
        else:
            self.merger_init = Merger_Adaptive.Merger_Adaptive

        self.test_mode = test_mode

    # sorts the input
    def sort(self):
        """put the list in sorted order with some method"""
        raise NotImplementedError("sort(internal) is not implemented")


# sorts the input
def sort(self, input_list, k=2):
    """creates a sorter object and calls the sort method"""
    raise NotImplementedError("sort(external) is not implemented")