from Mergers import Merger
import math
from Support import ListSlice
from typing import List


class Merger_Adaptive(Merger.Merger):
    def __init__(self,
                 runs: List[ListSlice.ListSlice],
                 write_list_slice: ListSlice.ListSlice,
                 option_code: int = 1,
                 merger_ipq_init=False, test_mode=False):

        super().__init__(runs, write_list_slice, option_code, merger_ipq_init, test_mode)

    def merge(self):
        runs_with_infs = []
        internal_positions = []
        initial_values = []

        # creates data for each run
        for run in self.runs:
            # start of the run about to be copied in the runs_with_infs list
            internal_positions.append(len(runs_with_infs))

            # copy the elements over
            posn_in_run_list = run.start
            while posn_in_run_list < run.end:
                runs_with_infs.append(run.list[posn_in_run_list])
                posn_in_run_list += 1

            # add an inf to end the run
            runs_with_infs.append(math.inf)

            # add the first value of this run to the initial values list - used to create the merger
            initial_values.append(run.list[run.start])

        # second, update the first part of the merger function
        # create a merger, and all values needed to manage it
        our_merger_ipq = self.merger_ipq_init(initial_values, test_mode=self.test_mode)
        write_posn = self.write_list_slice.start

        # until writing is finished
        while write_posn < self.write_list_slice.end:
            # get the smallest run from the merger
            min_run, min_priority = our_merger_ipq.peek_at_lowest_priority_element()

            # output that value
            self.write_list_slice.list[write_posn] = min_priority
            write_posn += 1
            internal_positions[min_run] += 1

            # update the value in the merger
            our_merger_ipq.update_lowest_priority(runs_with_infs[internal_positions[min_run]])
