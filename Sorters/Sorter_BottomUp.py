from Sorters import Sorter_PingPong
import math
from Support import ListSlice
from Mergers import Merger_Adaptive, MergerIPQ_Dummy


class Sorter_PingPong_BottomUp(Sorter_PingPong.Sorter_PingPong):
    def __init__(self, input_list, k,
                 merger_ipq_init=MergerIPQ_Dummy.MergerIPQ_Dummy,
                 merger_init=Merger_Adaptive.Merger_Adaptive):
        super().__init__(input_list, k, merger_ipq_init, merger_init)

        self.sorted = False

    # sorts the input
    def sort(self):
        self.merge_sort_k_fixed_length()

    # returns the input list
    def get_input_list(self):
        return self.input_list

    # ensures that the sorted list exists, and is sorted, then returns it
    def get_sorted_list(self):
        if not self.sorted:
            self.sort()

        return self.get_read_list()

    # sorts the elements using k way merge sort with fixed length runs
    def merge_sort_k_fixed_length(self):
        run_length = 1

        # while the array isn't sorted
        while run_length < self.input_length:
            read_list = self.get_read_list()

            # a block consists of k runs, and is merged in a single step
            number_of_blocks = math.ceil(self.input_length / (self.k * run_length))
            for block_number in range(number_of_blocks):

                runs = []
                # initialise run_start - run end doesn't need initialising
                run_start = block_number * run_length * self.k

                for run in range(self.k):
                    run_end = min(run_start + run_length, self.input_length)
                    runs.append(ListSlice.ListSlice(read_list, run_start, run_end))

                    run_start += run_length

                    # don't add nonsense runs when you run out of stuff to put in them
                    if run_start >= self.input_length:
                        break

                write_list_slice = ListSlice.ListSlice(self.get_write_list(), runs[0].start, runs[-1].end)

                # merge, using an external merger object
                our_merger = self.merger_init(runs, write_list_slice)
                our_merger.merge()

            # swap the ping and pong arrays
            self.read_ping_write_pong = not self.read_ping_write_pong
            run_length *= self.k

        self.sorted = True
