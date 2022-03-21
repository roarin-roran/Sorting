from Sorters import Sorter_PingPong
from Support import ListSlice
from Mergers import Merger_Adaptive, MergerIPQ_Dummy


class Sorter_PingPong_Adaptive(Sorter_PingPong.Sorter_PingPong):
    def __init__(self, input_list, k,
                 merger_ipq_init=MergerIPQ_Dummy.MergerIPQ_Dummy,
                 merger_init=Merger_Adaptive.Merger_Adaptive):
        super().__init__(input_list, k, merger_ipq_init, merger_init)

        self.sorted = False

    # sorts the input
    def sort(self):
        self.merge_sort_k_run_detection()

    # returns the input list
    def get_input_list(self):
        return self.input_list

    # ensures that the sorted list exists, and is sorted, then returns it
    def get_sorted_list(self):
        if not self.sorted:
            self.sort()

        return self.get_read_list()

    # a k way merge sorter using runs detected as a prepossessing step
    def merge_sort_k_run_detection(self):
        runs = self.detect_runs()

        while len(runs) > 1:
            block_number = 0

            # while we haven't overshot the last block
            while block_number < len(runs):
                # put all the runs for this block in a list, removing them from the main run list
                this_block_runs = []
                for run_number in range(block_number, min(block_number + self.k, len(runs))):
                    this_block_runs.append(runs.pop(block_number))

                # get a list slice for the merger to write to
                write_start = this_block_runs[0].start
                write_end = this_block_runs[-1].end
                this_block_write_list_slice = ListSlice.ListSlice(self.get_write_list(), write_start, write_end)

                # merge, using an external merger object
                our_merger = self.merger_init(this_block_runs, this_block_write_list_slice,
                                              merger_ipq_init=self.merger_ipq_init)
                new_run = our_merger.merge()

                # insert the new run in place of the old
                runs.insert(block_number, new_run)

                block_number += 1

            self.read_ping_write_pong = not self.read_ping_write_pong

        self.sorted = True

    # detects runs, returning a list of list slices - each of the one run
    def detect_runs(self):
        runs = []

        run_start = 0
        last_element_current_run = self.input_list[0]
        read_list = self.get_read_list()

        for index in range(len(self.input_list)):
            element = self.input_list[index]

            if element < last_element_current_run:
                runs.append(ListSlice.ListSlice(read_list, run_start, index))
                # start of the next run
                run_start = index

            last_element_current_run = element

        runs.append(ListSlice.ListSlice(read_list, run_start, len(self.input_list)))

        return runs
