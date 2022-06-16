from Sorters import Sorter_Adaptive
from Mergers import Merger_TwoWay


class Sorter_Adaptive_k_2(Sorter_Adaptive.Sorter_PingPong_Adaptive):
    def __init__(self, input_list, k=2,
                 merger_ipq_init=None,
                 merger_init=Merger_TwoWay.Merger_TwoWay,
                 test_mode=False):
        # todo - handle overrides and weird input

        if k != 2:
            raise ValueError("Sorter_Adaptive_k_2 is not defined for k =", k)

        if merger_ipq_init:
            raise ValueError("Sorter_Adaptive_k_2 does not use any ipq, yet", merger_ipq_init, "is specified")

        # if no override is selected, use this default
        if not merger_init:
            merger_init = Merger_TwoWay.Merger_TwoWay

        super().__init__(input_list, k=2, merger_ipq_init=None, merger_init=merger_init,
                         test_mode=test_mode)


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_Adaptive_k_2(input_list, k)
    sorter.sort()
