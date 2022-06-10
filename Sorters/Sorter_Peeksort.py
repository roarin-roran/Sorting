from Sorters import Sorter
from Support import ListSlice
import random
import copy

# todo: document conventions used wrt inclusive or exclusive parts of the list in function parameters
#  (specifically that an *exclusive* convention should be used throughout - though is probably not what's actually used
#  everywhere)


class Sorter_Peeksort(Sorter.Sorter):
    def __init__(self, input_list, k,
                 merger_ipq_init=False,
                 merger_init=False,
                 test_mode=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

        # used for merging
        self.temp_list = [-1]*len(input_list)

        # defined globally to easily return from a function
        self.next_input_start = 0
        self.next_first_run_end = 0

    def sort(self):
        """put the list in sorted order using k way peeksort"""

        # comes out 1 too long because of differences in convention?
        first_run_end = self._extend_run_right(0, len(self.input_list))
        # first_run_end = 0

        if first_run_end < len(self.input_list):
            #  extend run left returns the wrong answer when the initial run covers the whole input
            last_run_start = self._extend_run_left(len(self.input_list) - 1, first_run_end - 1)
        else:
            last_run_start = len(self.input_list)

        self._recursively_sort(0, first_run_end, last_run_start, len(self.input_list))

    # todo - increase efficiency by defining these in self instead of passing them?
    def _recursively_sort(self, input_start, first_run_end, last_run_start, input_end):
        """recursively sort an input assumed to contain at least two runs"""

        # todo - replace this with a global list of some clever size and access convention (size O(k log n)? access by
        #  noting the position locally, but accessing the list globally)
        merge_stack = [ListSlice.ListSlice([0], 0, 1)] * (self.k+2)
        next_merge_stack_index = 0

        # if the input is a single run - return
        if self._test_for_single_run(input_start, first_run_end, last_run_start, input_end):
            return
        # 1. test for and handle inputs with at most k inputs that aren't in known runs.
        #   (note that inputs where the first run overlaps the second are illegal)
        # todo - this base case is a hack, and should be replaced with alternatives. also - some experimentation should
        #  be used to find the appropriate base case size
        elif last_run_start - first_run_end <= self.k:
            self._handle_trivial_input(input_start, first_run_end, last_run_start, input_end,
                                       merge_stack, next_merge_stack_index)
        else:
            # 2. and 3. find all m values outside of a known run
            m = self._generate_initial_m_values(input_start, first_run_end, last_run_start, input_end)

            if len(m) > 0:
                # 6. initialise the dangling end
                self.next_input_start = input_start
                self.next_first_run_end = first_run_end

                # 4. generate recursive calls and merges using these m values
                i = 0
                while i < len(m):
                    # 5. find the left edge of the run (extend run left)
                    l_i = self._extend_run_left(m[i], self.next_first_run_end)

                    # note that step 6 has been moved - paper algorithm should be updated to reflect the current
                    # implementation

                    # 7. find the rightmost edge of the run (extend run right)
                    r_i = self._extend_run_right(m[i], last_run_start)

                    # 8. if any other m_i values are in this run: discard them, recurse on the dangly bit, merge the run
                    m_values_to_skip = self._count_skipped_m_values(m, i, r_i)

                    if m_values_to_skip:
                        # increment i to skip the runs
                        i += m_values_to_skip

                        # if there's anything to recurse on
                        if self.next_input_start < l_i:
                            # recurse on the dangly bit (if it isn't just a run) and throw it on the merge stack
                            next_input_start_copy = self.next_input_start
                            if self.next_first_run_end < l_i:
                                self._recursively_sort(self.next_input_start, self.next_first_run_end, l_i, l_i)

                            self._add_to_merge_stack(next_input_start_copy, l_i, merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1
                        # throw the discovered run on the merge stack
                        self._add_to_merge_stack(l_i, r_i, merge_stack, next_merge_stack_index)
                        next_merge_stack_index += 1
                        self.next_input_start = r_i
                        self.next_first_run_end = r_i

                    # 9. if not, it depends on whether m_i is closer to l_i or r_i
                    else:
                        if m[i] - l_i <= r_i - m[i]:
                            # if there's an unsorted portion, recurse on it and throw it on the merge stack
                            if self.next_first_run_end < l_i:
                                # end is l_i+1 because ends are exclusive
                                next_input_start_copy = self.next_input_start
                                self._recursively_sort(self.next_input_start, self.next_first_run_end, l_i, l_i)
                                self._add_to_merge_stack(next_input_start_copy, l_i,
                                                         merge_stack, next_merge_stack_index)
                                next_merge_stack_index += 1
                            # else if there's just a run, throw it on the stack without recursing first
                            elif self.next_input_start < l_i:
                                self._add_to_merge_stack(self.next_input_start, l_i,
                                                         merge_stack, next_merge_stack_index)
                                next_merge_stack_index += 1

                            # this run defines the start of the new dangly bit
                            self.next_input_start = l_i
                            self.next_first_run_end = r_i
                        else:
                            # recurse on the dangly bit if it isn't a run
                            next_input_start_copy = self.next_input_start
                            if self.next_input_start < l_i:
                                self._recursively_sort(next_input_start_copy, self.next_first_run_end, l_i, r_i)

                            # there always must be a run, even if it's just a single character.
                            self._add_to_merge_stack(next_input_start_copy, r_i, merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1

                            # the next dangly bit start without a run.
                            self.next_input_start = r_i
                            self.next_first_run_end = r_i

                    i += 1

                # 10. handle the last non-run section, and the final run.
                # if there's a non-run before the last run, recurse on the last section
                if self.next_input_start < last_run_start:
                    next_input_start_copy = self.next_input_start
                    self._recursively_sort(self.next_input_start, self.next_first_run_end, last_run_start, input_end)
                    self._add_to_merge_stack(next_input_start_copy, input_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1
                # if there's not, but there is a run - throw it on the merge stack
                elif last_run_start < input_end:
                    self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1
                # if neither is true, no action is required.
            else:
                if (first_run_end - input_start) > (input_end - last_run_start):
                    # throw the first run on the merge stack, recurse on the rest
                    self._add_to_merge_stack(input_start, first_run_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1
                    self._recursively_sort(first_run_end, first_run_end, last_run_start, input_end)
                    self._add_to_merge_stack(first_run_end, input_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1

                else:
                    # recurse on the first bit, throw the last run on the stack
                    self._recursively_sort(input_start, first_run_end, last_run_start, last_run_start)
                    self._add_to_merge_stack(first_run_end, last_run_start, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1

                    self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1

            # if there are multiple things on the merge stack - merge them, if not - don't bother
            if next_merge_stack_index > 1:
                self._merge(input_start, input_end, merge_stack, next_merge_stack_index)

        # return when everything that was passed in is a single run
        return

    # todo - lean more heavily on this, it was implemented after a bunch of other systems were working, some of them
    #  might not be needed
    def _test_for_single_run(self, input_start, first_run_end, last_run_start, input_end):
        unsorted_section_start = max(input_start, first_run_end)
        unsorted_section_end = min(last_run_start, input_end)

        # if the middle section exists
        if unsorted_section_end != unsorted_section_start:
            # test the middle section
            current_element = self.input_list[unsorted_section_start]
            for index in range(unsorted_section_start + 1, unsorted_section_end):
                if self.input_list[index] < current_element:
                    return False
                else:
                    current_element = self.input_list[index]

            # if the first run exists, test the boundary
            if input_start != first_run_end:
                if self.input_list[unsorted_section_start] < self.input_list[unsorted_section_start - 1]:
                    return False

            # if the last run exists, test the boundary
            if last_run_start != input_end:
                if self.input_list[unsorted_section_end - 1] > self.input_list[unsorted_section_end]:
                    return False
        else:
            # if there's no middle section, test if both runs exist
            if input_start != first_run_end and last_run_start != input_end:
                # if they do, test the boundary
                if self.input_list[first_run_end] < self.input_list[first_run_end - 1]:
                    return False

        # all failed tests cause the function to return false - if we get this far, they're all passed.
        return True

    def _handle_trivial_input(self, input_start, first_run_end, last_run_start, input_end,
                              merge_stack, next_merge_stack_index):
        # add the first run
        if input_start != first_run_end:
            self._add_to_merge_stack(input_start, first_run_end, merge_stack, next_merge_stack_index)
            next_merge_stack_index += 1

        # add middle elements, if any
        for index in range(first_run_end, last_run_start):
            self._add_to_merge_stack(index, index + 1, merge_stack, next_merge_stack_index)
            next_merge_stack_index += 1

        if last_run_start != input_end:
            # add the final run, if it exists
            self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
            next_merge_stack_index += 1

        self._merge(input_start, input_end, merge_stack, next_merge_stack_index)

    def _generate_initial_m_values(self, input_start, first_run_end, last_run_start, input_end):
        step = (input_end - input_start) / self.k
        trim_from_front = 0
        for i in range(0, self.k - 1):
            current_index = input_start + round(step*(i+1))
            if current_index <= first_run_end:
                trim_from_front += 1
            else:
                break

        trim_from_back = 0
        for i in range(trim_from_front + 1, self.k - 1):
            current_index = input_start + round(step*(i+1))
            if current_index >= last_run_start:
                trim_from_back += 1

        m = [-1] * (self.k - 1 - trim_from_front - trim_from_back)
        j = 0
        for i in range(trim_from_front, self.k - 1 - trim_from_back):
            m[j] = input_start + round(step*(i+1))
            j += 1

        return m

    def _extend_run_left(self, m_i, next_first_run_end):
        l_i = m_i
        while l_i > next_first_run_end:
            if self.input_list[l_i - 1] <= self.input_list[l_i]:
                l_i -= 1
            else:
                break

        return l_i

    def _extend_run_right(self, m_i, last_run_start):
        r_i = m_i
        while r_i < last_run_start - 1:
            if self.input_list[r_i + 1] >= self.input_list[r_i]:
                r_i += 1
            else:
                break

        return r_i + 1

    def _add_to_merge_stack(self, run_start, run_end, merge_stack, next_merge_stack_index):
        merge_stack[next_merge_stack_index] = ListSlice.ListSlice(self.input_list, run_start, run_end)

    def _merge(self, input_start, input_end, merge_stack, next_merge_stack_index):
        # todo - update to generate runs in a memory efficient way, rendering the slice unnecesary

        our_merger = self.merger_init(merge_stack[:next_merge_stack_index],
                                      ListSlice.ListSlice(self.temp_list, input_start, input_end),
                                      test_mode=self.test_mode)
        our_merger.merge()

        # note that this step is inefficient, and improving it is listed as issue #68 on github.
        for index in range(input_start, input_end):
            self.input_list[index] = self.temp_list[index]

    @staticmethod
    def _count_skipped_m_values(m, i, r_i):
        m_values_to_skip = 0
        # for all m values after the current one.
        for j in range(i + 1, len(m)):
            if m[j] <= r_i:
                m_values_to_skip += 1
            else:
                break

        return m_values_to_skip


# class Tester_Sorter_PeekSort(unittest.TestCase):

#     def test_merge_stack(self, input_start, input_end, merge_stack, next_merge_stack_index):
#         # print("testing merge stack (silent pass)")
#         # print("merge stack (ignore after", next_merge_stack_index, "):")
#         # for thing in merge_stack:
#             # print("\t", str(thing))
#         # print("\\end")
#         last_end = input_start
#         merge_length = 0
#         for index in range(next_merge_stack_index):
#             run = merge_stack[index]

#             # print(str(run), run.start, input_start)
#             self.assertEqual(last_end, run.start)
#             merge_length += run.end - run.start
#             last_end = run.end

#         self.assertEqual((input_end - input_start), merge_length)


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    our_peek_sorter = Sorter_Peeksort(input_list, k)
    our_peek_sorter.sort()


def run_all(input_list, k):
    all_fine = True

    for current_input in input_list:
        unsorted_input = current_input.copy()
        print("test case:", unsorted_input)
        sort(current_input, k)

        if current_input != sorted(current_input):
            print("input: ", current_input, "wasn't sorted correctly!")
            print("output:", current_input)
            all_fine = False
            input()
        else:
            print("sorts correctly\n")
            pass

    if all_fine:
        print("test performed - it's all still working")
        pass


# todo: convert most of these into additional formal tests in test_sorter
def run_test_cases():

    # trivial, unsorted inputs
    input_1 = [4, 3, 2, 1]
    input_2 = [4, 3, 2, 1, 5, 7, 6, 8]
    # fully sorted input
    input_3 = [1, 2, 3, 4, 5, 6, 7, 8]

    # reproducible random input
    input_4 = list(range(10))
    random.seed(12345678)
    random.shuffle(input_4)

    # edge case: long run in the middle of an input, with random stuff on either side
    # (intended for use with k=2 and k=4)
    input_5 = [4, 2, 3, 1, 5, 6, 7, 8, 11, 12, 10, 9]

    # edge case: mostly sorted inputs, with one unsorted character on the left or right
    input_6 = [5, 1, 2, 3, 4, 6, 7, 8]
    input_7 = [1, 2, 3, 4, 6, 7, 8, 5]

    # edge case: r_i closer, all dangly bit is sorted
    input_8 = [4, 5, 1, 2, 7, 3, 6, 8]

    # input which should merge without recursion with k >= 2
    input_9 = [2, 4, 6, 8, 1, 10, 11, 12, 3, 5, 7, 9]

    # longer reproducible random input - known bug
    input_10 = list(range(24))
    random.seed(12345678)
    random.shuffle(input_10)

    # shortest reproducible random input with the known bug:
    input_11 = list(range(19))
    random.seed(12345678)
    random.shuffle(input_11)

    input_12 = list(range(100))
    random.seed(12345678)
    random.shuffle(input_12)

    input_13 = [5, 6, 7, 8, 1, 2, 3, 4]

    all_inputs = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11,
                  input_12, input_13]

    # uncomment to check that all sortable inputs are still sorting correctly
    run_all(copy.deepcopy(all_inputs), 2)
    run_all(copy.deepcopy(all_inputs), 3)
    run_all(copy.deepcopy(all_inputs), 4)
    run_all(copy.deepcopy(all_inputs), 5)
    run_all(copy.deepcopy(all_inputs), 6)
    run_all(copy.deepcopy(all_inputs), 7)
    run_all(copy.deepcopy(all_inputs), 8)
    run_all(copy.deepcopy(all_inputs), 16)
    run_all(copy.deepcopy(all_inputs), 32)
    run_all(copy.deepcopy(all_inputs), 64)


# run_test_cases()
