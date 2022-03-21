from Sorters import Sorter


class Sorter_Default(Sorter.Sorter):
    def __init__(self, input_list, k,
                 merger_ipq_init=False,
                 merger_init=False):
        super().__init__(input_list, k)

        self.sortedList = False

    def sort(self):
        self.sortedList = self.input_list.copy()
        self.sortedList.sort()

    # returns the input list
    def get_input_list(self):
        return self.input_list

    # ensures that the sorted list exists, and is sorted, then returns it
    def get_sorted_list(self):
        if not self.sortedList:
            self.sort()

        return self.sortedList

