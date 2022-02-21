# major updates:
# 1. run detection
# 2. virtual sentinels
# 3. real IPQ
# 4. top down
# 4. galloping merge


# small improvements:
# 1. make mergerIPQ return the priority and the index
# 2. infrastructure for multiple mergerIPQ implementations, using a variable passed to init
# 3. basic test suite - random inputs and timing, output to screen
# 4. local k value for the ends - no point in having more than 50% of runs empty in a merge


from SimpleMergerPQ import SimpleMergerPQ as Merger
import math


class KWayMergeSorter:
    def __init__(self, input_array, k):
        self.inputArray = input_array
        self.k = k

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

    # sorts the elements using k way merge sort
    def merge_sort_k(self):
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

        print("merging from", read_list)
        print("starting at element", start_point, "with run length", run_length)

        # create runs_with_infs, internal_positions, and first_values_of_runs
        prep = self.prepare_merge_k_runs_fixed_length(start_point, run_length)

        runs_with_infs = prep[0]
        internal_positions = prep[1]
        first_values_of_runs = prep[2]

        # create a merger, and all values needed to manage it
        our_merger = Merger(first_values_of_runs)
        write_posn = start_point
        write_end = min((start_point + run_length * self.k), len(write_list))

        # until writing is finished
        while write_posn < write_end:
            # get the smallest run from the merger
            min_run = our_merger.peek_at_lowest_priority_element()

            # output that value
            write_list[write_posn] = runs_with_infs[internal_positions[min_run]]
            write_posn += 1
            internal_positions[min_run] += 1

            # update the value in the merger
            our_merger.update_lowest_priority(runs_with_infs[internal_positions[min_run]])

    # creates a temp list with the runs needed, followed by infs, and the internal positions of run starts within
    # that list
    def prepare_merge_k_runs_fixed_length(self, start_point, run_length):
        read_list = self.get_read_list()
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


input1 = [1, 3, 2, 4, 9, 8, 7]

ourKWMS = KWayMergeSorter(input1, k=3)
# ourKWMS.merge_sort_k()
# ourKWMS.merge_k_runs_fixed_length(start_point=0, run_length=2)
# ourKWMS.merge_k_runs_fixed_length(start_point=3, run_length=1)
# ourKWMS.merge_k_runs_fixed_length(start_point=4, run_length=1)

ourKWMS.merge_sort_k()
print(ourKWMS.get_read_list())
