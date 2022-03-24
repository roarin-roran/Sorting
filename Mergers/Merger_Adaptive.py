from Mergers import Merger
import math
from Support import ListSlice
from typing import List


class Merger_Adaptive(Merger.Merger):
    """merges elements from a list of slices into an output slice, adapting to variable run length by using real
    sentinels (infs at the end of runs - not the most efficient option possible)"""
    def __init__(self,
                 runs: List[ListSlice.ListSlice],
                 write_list_slice: ListSlice.ListSlice,
                 option_code: int = 2,
                 merger_ipq_init=False, test_mode=False):

        super().__init__(runs, write_list_slice, option_code, merger_ipq_init, test_mode)

    def merge(self):
        """merges the elements passed at object creation by modifying the original list, modifying the write slice"""
        # create an ipq, and all values needed to manage it
        initial_values = [0]*len(self.runs)
        absolute_internal_positions = [0]*len(self.runs)
        run_number = 0
        for run in self.runs:
            initial_values[run_number] = run.list[run.start]
            absolute_internal_positions[run_number] = run.start

            run_number += 1

        our_merger_ipq = self.merger_ipq_init(initial_values, test_mode=self.test_mode)

        write_posn = self.write_list_slice.start

        # until writing is finished
        while write_posn < self.write_list_slice.end:
            # get the smallest run from the merger
            min_run, min_priority = our_merger_ipq.peek_at_lowest_priority_element()

            # output that value
            self.write_list_slice.list[write_posn] = min_priority
            write_posn += 1

            absolute_internal_positions[min_run] += 1

            # update the ipq
            if absolute_internal_positions[min_run] >= self.runs[min_run].end:
                our_merger_ipq.update_lowest_priority(math.inf)
            else:
                next_value = self.runs[min_run].list[absolute_internal_positions[min_run]]

                our_merger_ipq.update_lowest_priority(next_value)


# todo - currently not tested, add tests back
class Merger_Adaptive_Real_Sentinels(Merger.Merger):
    """merges elements from a list of slices into an output slice, adapting to variable run length by using real
    sentinels (infs at the end of runs - not the most efficient option possible)

    deprecated method retained for time trials. the use of real sentinels is expected to be substantially worse than
    virtual sentinels"""
    def __init__(self,
                 runs: List[ListSlice.ListSlice],
                 write_list_slice: ListSlice.ListSlice,
                 option_code: int = 1,
                 merger_ipq_init=False, test_mode=False):

        super().__init__(runs, write_list_slice, option_code, merger_ipq_init, test_mode)

    def merge(self):
        """merges the elements passed at object creation by modifying the original list, modifying the write slice"""
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
