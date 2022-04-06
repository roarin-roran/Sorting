from Sorters import Sorter


class Sorter_Default(Sorter.Sorter):
    """a wrapper class """

    def __init__(self, input_list,
                 k=2,
                 merger_ipq_init=False,
                 merger_init=False,
                 test_mode=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

        self.sorted = False

    def sort(self):
        self.input_list.sort()
        self.sorted = True

        return self.input_list


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_Default(input_list)
    sorter.sort()
