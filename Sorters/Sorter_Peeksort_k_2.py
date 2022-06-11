from Sorters import Sorter_Peeksort
from Mergers import Merger_Two_Way


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    print("WARNING: currently broken")
    input()

    # todo - fix this class. currently, peeksort sometimes uses k=3 even when k is set to 2. it has a fair few issues...
    sorter = Sorter_Peeksort.Sorter_Peeksort(input_list, 2, merger_init=Merger_Two_Way.Merger_Two_Way)
    sorter.sort()
