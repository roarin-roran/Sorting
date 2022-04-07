from Sorters import Sorter_PingPong
from Support import ListSlice
import copy


class Sorter_PingPong_Adaptive(Sorter_PingPong.Sorter_PingPong):
    def __init__(self, input_list, k,
                 merger_ipq_init=False,
                 merger_init=False,
                 test_mode=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

    def sort(self):
        """sorts the input using a bottom up k-way run adaptive merge sort. runs are detected as a pre-processing step,
        then merged k at a time until one run remains, with no """
        runs = self.detect_runs()

        # while multiple runs remain
        while len(runs) > 1:
            block_number = 0

            # while we haven't overshot the last block
            while block_number < len(runs):
                # test for a single block run - this is already merged.
                if block_number + 1 == len(runs):
                    break

                # todo - initialise this_block_runs instead of appending to it
                # todo - setup ping pong here for the runs array, copying existing code.
                # array length is going to reduce as we go - need an "end of array" value recorded for end of the
                # sensible bit

                # put all the runs for this block in a list, removing them from the main run list

                this_block_runs = [runs[0]]*(min(block_number + self.k, len(runs)) - block_number)
                for i in range(len(this_block_runs)):
                    this_block_runs[i] = runs.pop(block_number)

                # get a list slice for the merger to write to
                write_start = this_block_runs[0].start
                write_end = this_block_runs[-1].end
                this_block_write_list_slice = ListSlice.ListSlice(self.get_write_list(), write_start, write_end)

                # merge, using an external merger object
                our_merger = self.merger_init(this_block_runs, this_block_write_list_slice,
                                              merger_ipq_init=self.merger_ipq_init,
                                              test_mode=self.test_mode)
                our_merger.merge()

                # insert the new run in place of the old
                runs.insert(block_number, this_block_write_list_slice)

                block_number += 1

            self.read_ping_write_pong = not self.read_ping_write_pong

        # if the sorted and original lists are different, copy the sorted list into the original list
        read_list = self.get_read_list()
        if read_list != self.input_list:
            for i in range(len(self.input_list)):
                self.input_list[i] = read_list[i]

        return self.input_list

    def detect_runs(self):
        """detects runs, returning them as a list of list slices"""
        runs = []

        run_start = 0
        last_element_current_run = self.input_list[0]
        read_list = self.get_read_list()

        # for every input element
        for index in range(len(self.input_list)):
            element = self.input_list[index]

            # if it breaks the run, start a new one
            if element < last_element_current_run:
                runs.append(ListSlice.ListSlice(read_list, run_start, index))
                # start of the next run
                run_start = index

            last_element_current_run = element

        runs.append(ListSlice.ListSlice(read_list, run_start, len(self.input_list)))

        return runs


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_PingPong_Adaptive(input_list, k)
    sorter.sort()
