# notes:
# 1. at some point, "day trip" array management will be used in place of ping pong, for methods like powersort
#   which lack clear run definitions
from Mergers import Merger_Adaptive
from Merger_IPQs import MergerIPQ_Dummy


class Sorter:
    def __init__(self, input_list,
                 k=2,
                 merger_ipq_init=False,
                 merger_init=False):
        self.input_list = input_list
        self.k = k

        if merger_ipq_init:
            self.merger_ipq_init = merger_ipq_init
        else:
            self.merger_ipq_init = MergerIPQ_Dummy.MergerIPQ_Dummy

        if merger_init:
            self.merger_init = merger_init
        else:
            self.merger_init = Merger_Adaptive.Merger_Adaptive

    # sorts the input
    def sort(self):
        raise NotImplementedError("sort is not implemented")
