# notes:
# 1. at some point, "day trip" array management will be used in place of ping pong, for methods like powersort
#   which lack clear run definitions

import SimpleMergerPQ
import math
import numpy as np


class KWayMergeSorter:
    def __init__(self, input_array, k, merger_init=SimpleMergerPQ.SimpleMergerPQ):
        self.inputArray = input_array
        self.k = k
        self.merger_init = merger_init

        self.input_length = len(input_array)

        self.ping = input_array.copy()
        self.pong = input_array.copy()

        self.read_ping_write_pong = True

    # read and write lists change - returns the internal list being read from
    def get_read_list(self):
        if self.read_ping_write_pong:
            return self.ping
        else:
            return self.pong

    # read and write list change - returns the internal list being written to
    def get_write_list(self):
        if self.read_ping_write_pong:
            return self.pong
        else:
            return self.ping

    # * * * * * * * * * ** * * * * * * * * * *
    # * * * * * NON-ADAPTIVE SORTING * * * * *
    # * * * * * * * * * ** * * * * * * * * * *

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

    # * * * * * * * * * *  * * * * * * * * *
    # * * * * * * ADAPTIVE SORTING * * * * *
    # * * * * * * * * * *  * * * * * * * * *

    # a k way merge sorter using runs detected as a preprocessing step
    def merge_sort_k_run_detection(self):
        start_points, end_points = self.detect_runs()

        while len(start_points) > 1:
            block_number = 0

            while block_number < len(start_points):
                next_block_starts = ListSlice(start_points, block_number, min(block_number + self.k, len(start_points)))
                next_block_ends = ListSlice(end_points, block_number, min(block_number + self.k, len(end_points)))

                self.merge_k_runs_variable_length(next_block_starts, next_block_ends)

                # remove all but the start of the new run from start_points
                start_points = next_block_starts.list[0:next_block_starts.start + 1] + \
                    next_block_starts.list[next_block_starts.end:]

                # remove all but the end of the new run from end_points
                end_points = next_block_ends.list[0:next_block_ends.start] + \
                    next_block_ends.list[next_block_ends.end - 1:]

                block_number += 1

            self.read_ping_write_pong = not self.read_ping_write_pong

        print("sorted!")
        print(self.get_read_list())

    # merges k runs as defined by their start and end points, inputted as ListSlice objects
    def merge_k_runs_variable_length(self, start_points, end_points):
        read_list = self.get_read_list()
        write_list = self.get_write_list()

        # create runs_with_infs, internal_positions, and first_values_of_runs
        runs_with_infs, internal_positions, first_values_of_runs = \
            KWayMergeSorter.prep_merge_k_runs_variable_length(read_list, start_points, end_points)

        # create a merger, and all values needed to manage it
        our_merger = self.merger_init(first_values_of_runs)
        write_posn = start_points.list[start_points.start]
        # accessing the last element, inclusively
        write_end = end_points.list[end_points.end - 1]

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
    # that list, used for variable length k-way merging
    @staticmethod
    def prep_merge_k_runs_variable_length(read_list, start_points, end_points):
        read_list_posn = start_points.list[start_points.start]

        runs_with_infs = []
        internal_positions = []
        initial_values = []

        # creates data for each run
        # note - end of input handled by creating runs of length 0 - probably not optimal
        for run_number in range(start_points.end - start_points.start):
            # start of the run about to be copied
            internal_positions.append(len(runs_with_infs))

            # copy the elements over
            while read_list_posn < end_points.list[end_points.start + run_number]:
                runs_with_infs.append(read_list[read_list_posn])
                read_list_posn += 1

            # add an inf to end the run
            runs_with_infs.append(math.inf)

            # add the first value of this run to the initial values list - used to create the merger
            initial_values.append(runs_with_infs[internal_positions[run_number]])

        return [runs_with_infs, internal_positions, initial_values]

    # returns arrays containing the starts and ends of all runs in the input
    def detect_runs(self):
        start_points = [0]
        end_points = []

        last_element_current_run = self.inputArray[0]

        for index in range(len(self.inputArray)):
            element = self.inputArray[index]

            if element < last_element_current_run:
                end_points.append(index)
                start_points.append(index)

            last_element_current_run = element

        end_points.append(len(self.inputArray))

        return start_points, end_points


class ListSlice:
    def __init__(self, sliced_list, start, end):
        self.list = sliced_list
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.list[self.start:self.end])

    def get_list(self):
        return self.list[self.start:self.end]


input1 = [1, 3, 2, 4, 9, 8, 7]
input2 = [4, 6, 12, 3, 5, 70, 2, 7, 48, 80, 1]
random_input = np.random.randint(1, 50, 50)

ourKWMS = KWayMergeSorter(random_input, k=4)

# ourKWMS.merge_sort_k()
# ourKWMS.merge_k_runs_fixed_length(start_point=0, run_length=2)
# ourKWMS.merge_k_runs_fixed_length(start_point=3, run_length=1)
# ourKWMS.merge_k_runs_fixed_length(start_point=4, run_length=1)

# ourKWMS.merge_sort_k_fixed_length()
# print(ourKWMS.get_read_list())

# ourKWMS.merge_k_runs_variable_length([0, 2, 4], [2, 4, 5])
# ourKWMS.merge_k_runs_variable_length([0, 3, 6], [3, 6, 10])

# ourKWMS.detect_runs()
ourKWMS.merge_sort_k_run_detection()
