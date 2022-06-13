from Sorters import Sorter_Adaptive
from Mergers import Merger_TwoWay


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_Adaptive.Sorter_PingPong_Adaptive(input_list, 2, merger_init=Merger_TwoWay.Merger_TwoWay)
    sorter.sort()
