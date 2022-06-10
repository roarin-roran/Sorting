from Sorters import Sorter_Peeksort
from Mergers import Merger_Two_Way


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_Peeksort.Sorter_Peeksort(input_list, 2, merger_init=Merger_Two_Way.Merger_Two_Way)
    sorter.sort()
