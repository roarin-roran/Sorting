import PingPongKWayMergeSorter
import SimpleMergerPQ
import math
import numpy as np


class SimpleKWayMergeSorter(PingPongKWayMergeSorter.PingPongKWayMergeSorter):
    def __init__(self, input_array, k, merger_init=SimpleMergerPQ.SimpleMergerPQ):
        self.inputArray = input_array
        self.k = k
        self.merger_init = merger_init

        super().__init__(input_array)

    # sorts the elements using k way merge sort with fixed length runs
    def merge_sort_k_fixed_length(self):
        run_length = 1

        # while the array isn't sorted
        while run_length < self.input_length:
            # a block consists of k runs, and is merged in a single step
            number_of_blocks = math.ceil(self.input_length / (self.k * run_length))
            for block_number in range(number_of_blocks):
                start_point = block_number * run_length * self.k
                self.merge_k_runs_fixed_length(start_point, run_length)

            # swap the ping and pong arrays
            self.read_ping_write_pong = not self.read_ping_write_pong
            run_length *= self.k

        print("sorted!")
        print(self.get_read_list())

    # merges k fixed length runs
    def merge_k_runs_fixed_length(self, start_point, run_length):
        read_list = self.get_read_list()
        write_list = self.get_write_list()

        # create runs_with_infs, internal_positions, and first_values_of_runs
        runs_with_infs, internal_positions, first_values_of_runs = \
            self.prepare_merge_k_runs_fixed_length(read_list, start_point, run_length)

        # create a merger, and all values needed to manage it
        our_merger = self.merger_init(first_values_of_runs)
        write_posn = start_point
        write_end = min((start_point + run_length * self.k), len(write_list))

        # until writing is finished
        while write_posn < write_end:
            # get the smallest run from the merger
            min_run, min_priority = our_merger.peek_at_lowest_priority_element()

            # output that value
            write_list[write_posn] = min_priority
            write_posn += 1
            internal_positions[min_run] += 1

            # update the value in the merger
            our_merger.update_lowest_priority(runs_with_infs[internal_positions[min_run]])

    # creates a temp list with the runs needed, followed by infs, and the internal positions of run starts within
    # that list, used for fixed length k-way merging
    def prepare_merge_k_runs_fixed_length(self, read_list, start_point, run_length):
        read_list_posn = start_point

        runs_with_infs = []
        internal_positions = []
        initial_values = []

        # creates data for each run
        # note - end of input handled by creating runs of length 0 - probably not optimal
        for run_number in range(self.k):
            # start of the run about to be copied
            internal_positions.append(len(runs_with_infs))

            # prevents list overrun
            end_of_run = min(len(read_list), start_point + (run_number + 1) * run_length)

            # copy the elements over
            while read_list_posn < end_of_run:
                runs_with_infs.append(read_list[read_list_posn])
                read_list_posn += 1

            # add an inf to end the run
            runs_with_infs.append(math.inf)

            # add the first value of this run to the initial values list - used to create the merger
            initial_values.append(runs_with_infs[internal_positions[run_number]])

        return [runs_with_infs, internal_positions, initial_values]


# input1 = [1, 3, 2, 4, 9, 8, 7]
# input2 = [4, 6, 12, 3, 5, 70, 2, 7, 48, 80, 1]
random_input = np.random.randint(1, 50, 50)

our_SKWMS = SimpleKWayMergeSorter(random_input, 2)
our_SKWMS.merge_sort_k_fixed_length()
