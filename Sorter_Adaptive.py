import Sorter_PingPong
import MergerPQ_Dummy
import ListSlice
import math


class Sorter_PingPong_Adaptive(Sorter_PingPong.Sorter_PingPong):
    def __init__(self, input_list, k, merger_init=MergerPQ_Dummy.MergerPQ_Dummy):
        self.input_list = input_list
        self.k = k
        self.merger_init = merger_init

        super().__init__(input_list)

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
        start_points, end_points = self.detect_runs()

        while len(start_points) > 1:
            block_number = 0

            while block_number < len(start_points):
                next_block_starts = ListSlice.ListSlice(start_points, block_number,
                                                        min(block_number + self.k, len(start_points)))
                next_block_ends = ListSlice.ListSlice(end_points, block_number,
                                                      min(block_number + self.k, len(end_points)))

                self.merge_k_runs_variable_length(next_block_starts, next_block_ends)

                # remove all but the start of the new run from start_points
                start_points = next_block_starts.list[0:next_block_starts.start + 1] + \
                    next_block_starts.list[next_block_starts.end:]

                # remove all but the end of the new run from end_points
                end_points = next_block_ends.list[0:next_block_ends.start] + \
                    next_block_ends.list[next_block_ends.end - 1:]

                block_number += 1

            self.read_ping_write_pong = not self.read_ping_write_pong

        self.sorted = True

    # merges k runs as defined by their start and end points, inputted as ListSlice objects
    def merge_k_runs_variable_length(self, start_points, end_points):
        read_list = self.get_read_list()
        write_list = self.get_write_list()

        # create runs_with_infs, internal_positions, and first_values_of_runs
        runs_with_infs, internal_positions, first_values_of_runs = \
            Sorter_PingPong_Adaptive.prep_merge_k_runs_variable_length(read_list, start_points, end_points)

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

        last_element_current_run = self.input_list[0]

        for index in range(len(self.input_list)):
            element = self.input_list[index]

            if element < last_element_current_run:
                end_points.append(index)
                start_points.append(index)

            last_element_current_run = element

        end_points.append(len(self.input_list))

        return start_points, end_points

