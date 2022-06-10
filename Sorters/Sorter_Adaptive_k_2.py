from Sorters import Sorter_Adaptive
from Mergers import Merger_Two_Way


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_Adaptive.Sorter_PingPong_Adaptive(input_list, 2, merger_init=Merger_Two_Way.Merger_Two_Way)
    sorter.sort()
