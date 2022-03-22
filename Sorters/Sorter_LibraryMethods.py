from Sorters import Sorter


class Sorter_Default(Sorter.Sorter):
    def __init__(self, input_list,
                 k=2,
                 merger_ipq_init=False,
                 merger_init=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init)

        self.sorted = False

    def sort(self):
        self.input_list.sort()
        self.sorted = True

        return self.input_list


