# notes:
# 1. at some point, "day trip" array management will be used in place of ping pong, for methods like powersort
#   which lack clear run definitions
from Mergers import Merger_Adaptive, MergerIPQ_Dummy


class Sorter:
    def __init__(self, input_list,
                 k=2,
                 merger_ipq_init=MergerIPQ_Dummy.MergerIPQ_Dummy,
                 merger_init=Merger_Adaptive.Merger_Adaptive):
        self.input_list = input_list
        self.k = k
        self.merger_ipq_init = merger_ipq_init
        self.merger_init = merger_init

    # sorts the input
    def sort(self):
        print("sort is not implemented")
        raise NotImplementedError

    # returns the input list
    def get_input_list(self):
        print("get_input_list is not implemented")
        raise NotImplementedError

    # returns the sorted list
    def get_sorted_list(self):
        print("get_sorted_list is not implemented")
        raise NotImplementedError
