from Mergers import Merger
from Support import ListSlice
from typing import List


class Merger_Two_Way(Merger.Merger):
    """a stripped down merger which only accepts two runs, and always uses k=2"""
    def __init__(self,
                 runs: List[ListSlice.ListSlice],
                 write_list_slice: ListSlice.ListSlice,
                 option_code: int = 3,
                 merger_ipq_init=False, test_mode=False):
        if len(runs) != 2:
            raise ValueError("Merger_Two_Way can only merge two runs, but", len(runs), "were inputted")

        super().__init__(runs, write_list_slice, option_code, merger_ipq_init, test_mode)

    def merge(self) -> ListSlice.ListSlice:
        """merges the elements passed at object creation by modifying the original list, modifying the write slice"""
        # initialise positions in input runs and output run
        left_run_index = self.runs[0].start
        right_run_index = self.runs[1].start
        output_index = self.write_list_slice.start

        while True:
            # if left run is to be used next
            if self.runs[0].list[left_run_index] <= self.runs[1].list[right_run_index]:
                # copy the next element over
                self.write_list_slice.list[output_index] = self.runs[0].list[left_run_index]
                left_run_index += 1

                # if this run is empty, copy the other over
                if left_run_index == self.runs[0].end:
                    while right_run_index < self.runs[1].end:
                        output_index += 1
                        self.write_list_slice.list[output_index] = self.runs[1].list[right_run_index]
                        right_run_index += 1
                    break
            # if the right run is to be used next
            else:
                # copy the next element over
                self.write_list_slice.list[output_index] = self.runs[1].list[right_run_index]
                right_run_index += 1

                # if this run is empty, copy the other over
                if right_run_index == self.runs[1].end:
                    while left_run_index < self.runs[0].end:
                        output_index += 1
                        self.write_list_slice.list[output_index] = self.runs[0].list[left_run_index]
                        left_run_index += 1
                    break

            # always copy an element, so always index the output.
            output_index += 1

        return self.write_list_slice
