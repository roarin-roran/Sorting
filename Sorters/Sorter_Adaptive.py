from Sorters import Sorter_PingPong
from Support import ListSlice


class Sorter_PingPong_Adaptive(Sorter_PingPong.Sorter_PingPong):
    def __init__(self, input_list, k,
                 merger_ipq_init=False,
                 merger_init=False,
                 test_mode=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

        self.runs_ping = self.detect_runs()
        # note that these objects don't need to be identical or different - just have the same size for efficient memory
        # allocation
        self.runs_pong = self.runs_ping.copy()
        self.runs_read_ping_write_pong = True

    def sort(self):
        """sorts the input using a bottom up k-way run adaptive merge sort. runs are detected as a pre-processing step,
        then merged k at a time until one run remains, with no """
        runs = self.runs_ping

        # while multiple runs remain
        while len(runs) > 1:
            block_number = 0

            # while we haven't overshot the last block
            while block_number < len(runs):
                # test for a single block run - this is already merged.
                if block_number + 1 == len(runs):
                    break

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

    def sort_new(self):
        # initialise these, as they're used before they would otherwise be set
        num_read_runs = len(self.get_runs_read_list())
        num_write_runs = len(self.get_runs_write_list())

        # while multiple runs remain
        while num_write_runs > 1:
            # start from the first block of runs, and the beginning of both the read and write lists of runs
            block_number = 0
            posn_in_read_runs = 0
            posn_in_write_runs = 0

            # while we haven't overshot the last block
            while posn_in_read_runs < num_read_runs:
                # form a block, either with the next k runs, or all remaining runs.
                block_end = min((block_number + 1)*self.k, num_read_runs)
                this_block_runs = self.get_runs_read_list()[block_number * self.k:block_end]

                # if multiple runs require merging
                if len(this_block_runs) > 1:
                    # get a list slice for the merger to write to
                    write_start = this_block_runs[0].start
                    write_end = this_block_runs[-1].end
                    this_block_write_list_slice = ListSlice.ListSlice(self.get_write_list(), write_start, write_end)

                    # merge, using an external merger object
                    our_merger = self.merger_init(this_block_runs, this_block_write_list_slice,
                                                  merger_ipq_init=self.merger_ipq_init,
                                                  test_mode=self.test_mode)
                    our_merger.merge()

                    # NOTE - currently this is only correct in the middle of a block, and doesn't matter at the end of
                    # the block. if the code is ever updated so that the value of posn_in_read_runs matters at the end
                    # of a block, this will cause an error... but I don't see that happening, and this is fast.
                    posn_in_read_runs += self.k

                    # the list slice that was modified now contains the new run - add it to the runs list
                    self.get_runs_write_list()[posn_in_write_runs] = this_block_write_list_slice
                    posn_in_write_runs += 1

                    block_number += 1
                else:
                    # one run is inherently sorted, so just copy it over
                    self.get_runs_write_list()[posn_in_write_runs] = this_block_runs[0]
                    posn_in_write_runs += 1

                    # if there's just one run, either k=1 and we're on a hiding to nothing, or we're at the end of a
                    # block and can break
                    break

            # flip between read and write arrays in all ping-pong managed memory
            self.read_ping_write_pong = not self.read_ping_write_pong
            self.runs_read_ping_write_pong = not self.runs_read_ping_write_pong

            # number of runs is the number we wrote this time around
            num_read_runs = posn_in_write_runs
            num_write_runs = posn_in_write_runs

        # if the sorted and original lists are different, copy the sorted list into the original list
        read_list = self.get_read_list()
        if read_list != self.input_list:
            for i in range(len(self.input_list)):
                self.input_list[i] = read_list[i]

        return self.input_list

    # choose and return the correct list
    def get_runs_read_list(self):
        if self.runs_read_ping_write_pong:
            return self.runs_ping
        else:
            return self.runs_pong

    # choose and return the correct list
    def get_runs_write_list(self):
        if self.runs_read_ping_write_pong:
            return self.runs_pong
        else:
            return self.runs_ping

    # a tostring method for the runs read list - being a list of objects, it can be unreadable. used for debugging
    def str_runs_read_list(self, length):
        runs_read_list = self.get_runs_read_list()
        output = []

        for run_number in range(length):
            output.append(str(runs_read_list[run_number]))

        return output

    # a tostring method for the runs write list - being a list of objects, it can be unreadable. used for debugging
    def str_runs_write_list(self, length):
        runs_write_list = self.get_runs_write_list()
        output = []
        for run_number in range(length):
            output.append(str(runs_write_list[run_number]))

        return output

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
