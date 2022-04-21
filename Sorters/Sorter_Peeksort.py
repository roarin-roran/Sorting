from Sorters import Sorter
from Support import ListSlice
import random
import unittest


# todo: document conventions used wrt inclusive or exclusive parts of the list in function parameters
#  (specifically that an *exclusive* convention is used throughout - though this should be confirmed by testing)

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

        # todo clarify what the hell is going on with these +1 and -1 values

        # comes out 1 too long because of differences in convention?
        # first_run_end = self._extend_run_right(0, len(self.input_list)) - 1
        first_run_end = 0

        # comes out 1 too short because reasons??
        # last_run_start = self._extend_run_left(len(self.input_list) - 1, first_run_end) + 1
        last_run_start = len(self.input_list)

        self._recursively_sort(0, first_run_end, last_run_start, len(self.input_list))

    # sorts the input
    # todo - increase efficiency by defining these in self instead of passing them
    def _recursively_sort(self, input_start, first_run_end, last_run_start, input_end):
        """recursively sort an input assumed to contain at least two runs"""

        # todo - replace the base case, and shrink this back down
        merge_stack = [ListSlice.ListSlice([0], 0, 1)] * self.k*2
        next_merge_stack_index = 0

        print("PASS START")
        print("beginning a recursive pass, with parameters:", input_start, first_run_end, last_run_start, input_end)
        print("and input list state", self.input_list)

        # if the input is a single run - return
        if self._test_for_single_run(input_start, input_end):
            print("PASS END (trivial)")
            return
        # 1. test for and handle inputs with at most k inputs that aren't in known runs.
        #   (note that inputs where the first run overlaps the second are illegal)
        elif last_run_start - first_run_end <= self.k:
            self._handle_trivial_input(input_start, first_run_end, last_run_start, input_end,
                                       merge_stack, next_merge_stack_index)
        else:
            # 2. and 3. find all m values outside of a known run
            m = self._generate_initial_m_values(input_start, first_run_end, last_run_start, input_end)

            # 6. initialise the dangling end
            self.next_input_start = input_start
            self.next_first_run_end = first_run_end

            # 4. generate recursive calls and merges using these m values
            i = 0
            while i < len(m):
                print("\tm_i:       ", m[i])

                # 5. find the left edge of the run (extend run left)
                l_i = self._extend_run_left(m[i], self.next_first_run_end)
                print("\tl_i:       ", l_i)

                # note that step 6 has been moved, and a rewrite is required because this is kinda confusing.

                # 7. find the rightmost edge of the run (extend run right)
                r_i = self._extend_run_right(m[i], last_run_start)
                print("\tr_i:       ", r_i)

                # 8. if any other m_i values are in this run: discard them, recurse on the dangly bit, merge the run
                m_values_to_skip = self._count_skipped_m_values(m, i, r_i)

                if m_values_to_skip:
                    print("\n\tskipping", m_values_to_skip, "m values, because they're contained in this run.")
                    # increment i to skip the runs
                    i += m_values_to_skip

                    # if there's anything to recurse on
                    if self.next_input_start < l_i:
                        # recurse on the dangly bit (if it isn't just a run) and throw it on the merge stack
                        next_input_start_copy = self.next_input_start
                        if self.next_first_run_end < l_i:
                            print("\t\trecurse on, position 1:",
                                  self.next_input_start, self.next_first_run_end, l_i, l_i)
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
                        print("\tl_i is closer(default)")
                        # if there's an unsorted portion, recurse on it and throw it on the merge stack
                        if self.next_first_run_end < l_i:
                            # end is l_i+1 because ends are exclusive
                            print("\t\trecurse on, position 2:",
                                  self.next_input_start, self.next_first_run_end, l_i, l_i)
                            next_input_start_copy = self.next_input_start
                            self._recursively_sort(self.next_input_start, self.next_first_run_end, l_i, l_i)
                            self._add_to_merge_stack(next_input_start_copy, l_i, merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1
                        # else if there's just a run, throw it on the stack without recursing first
                        elif self.next_input_start < l_i:
                            self._add_to_merge_stack(self.next_input_start, l_i, merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1

                        # this run defines the start of the new dangly bit
                        self.next_input_start = l_i
                        self.next_first_run_end = r_i
                    else:
                        print("\tr_i is closer")
                        # todo - test that this is necesary and sufficient
                        # recurse on the dangly bit if it isn't a run
                        next_input_start_copy = self.next_input_start
                        if self.next_input_start < l_i:

                            print("\t\trecurse on, position 3:",
                                  self.next_input_start, self.next_first_run_end, l_i, r_i)
                            self._recursively_sort(next_input_start_copy, self.next_first_run_end, l_i, r_i)

                        # there always must be a run, even if it's just a single character.
                        self._add_to_merge_stack(next_input_start_copy, r_i, merge_stack, next_merge_stack_index)
                        next_merge_stack_index += 1

                        # the next dangly bit start without a run.
                        # -1 to fix convention
                        self.next_input_start = r_i
                        self.next_first_run_end = r_i

                print("\tnext peek time!\n")
                i += 1

            # 10. handle the last non-run section, and the final run.
            print("\t handle last section")
            # if there's a non-run before the last run, recurse on the last section
            if self.next_input_start < last_run_start:
                next_input_start_copy = self.next_input_start
                print("\t\trecurse on, position 4:",
                      self.next_input_start, self.next_first_run_end, last_run_start, input_end)
                self._recursively_sort(self.next_input_start, self.next_first_run_end, last_run_start, input_end)
                self._add_to_merge_stack(next_input_start_copy, input_end, merge_stack, next_merge_stack_index)
                next_merge_stack_index += 1
            # if there's not, but there is a run - throw it on the merge stack
            elif last_run_start < input_end:
                self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
                next_merge_stack_index += 1
            # if neither is true, no action is required.

            # if there are multiple things on the merge stack - merge them, if not - don't bother
            if next_merge_stack_index > 1:
                print("time to merge the merge stack!\n")
                print("input_list before", self.input_list)

                our_tester = Tester_Sorter_PeekSort()
                our_tester.test_merge_stack(input_start, input_end, merge_stack, next_merge_stack_index)

                self._merge(input_start, input_end, merge_stack, next_merge_stack_index)
                print("input_list after", self.input_list)

        # return when everything that was passed in is a single run
        print("PASS END (nontrivial)")
        return

    # todo - make this method smarter, using the run boundaries
    # todo - lean more heavily on this, it was implemented after a bunch of other systems were working, some of them
    #  might not be needed
    def _test_for_single_run(self, input_start, input_end):
        current_element = self.input_list[input_start]
        for index in range(input_start, input_end):
            if self.input_list[index] >= current_element:
                current_element = self.input_list[index]
            else:
                return False

        return True

    def _handle_trivial_input(self, input_start, first_run_end, last_run_start, input_end,
                              merge_stack, next_merge_stack_index):
        print("handling trivial input")
        print(input_start, first_run_end)

        # add the first run
        if input_start != first_run_end:
            self._add_to_merge_stack(input_start, first_run_end, merge_stack, next_merge_stack_index)
            next_merge_stack_index += 1

        # add middle elements, if any
        for index in range(first_run_end, last_run_start):
            print("bing", index, index + 1, merge_stack, next_merge_stack_index)
            self._add_to_merge_stack(index, index + 1, merge_stack, next_merge_stack_index)
            print("bong")
            next_merge_stack_index += 1

        if last_run_start != input_end:
            # add the final run, if it exists
            self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
            next_merge_stack_index += 1

        self._merge(input_start, input_end, merge_stack, next_merge_stack_index)
        print("end handle of trivial input")

    # todo - write this without a list slice for cheaper memory interactions
    #   (try reducing the length of m at the beginning, then generating m_i values)
    def _generate_initial_m_values(self, input_start, first_run_end, last_run_start, input_end):
        # 2. create k-1 evenly spaced m_i values
        m = [0] * (self.k - 1)
        step = (input_end - input_start) / self.k

        for i in range(self.k - 1):
            m[i] = input_start + round(step * (i + 1))

        print("uncropped m:", m)

        # 3. remove any m_i values that are inside the start or end run
        m_start = 0
        for m_i in m:
            if m_i <= first_run_end:
                m_start += 1
            else:
                break

        m_end = len(m)
        for m_i in reversed(m):
            if m_i > last_run_start:
                m_end -= 1
            else:
                break

        print("cropped m:", m[m_start:m_end])

        if len(m[m_start:m_end]) == 0:
            print("no m!")
            input()

        return m[m_start:m_end]

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
        print("\t\tmerge:     ", run_start, run_end)

        merge_stack[next_merge_stack_index] = ListSlice.ListSlice(self.input_list, run_start, run_end)

    def _merge(self, input_start, input_end, merge_stack, next_merge_stack_index):
        # todo - update to generate runs in a memory efficient way, rendering the slice unnecesary

        print("merging the stack")

        our_merger = self.merger_init(merge_stack[:next_merge_stack_index],
                                      ListSlice.ListSlice(self.temp_list, input_start, input_end))
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

    def _dummy_recurse(self, input_start, first_run_end, last_run_start, input_end):
        print(self.input_list)
        print("dummy recursion: ", input_start, first_run_end, last_run_start, input_end)
        input()


class Tester_Sorter_PeekSort(unittest.TestCase):

    def test_merge_stack(self, input_start, input_end, merge_stack, next_merge_stack_index):
        print("testing merge stack (silent pass)")
        print("merge stack (ignore after", next_merge_stack_index, "):")
        for thing in merge_stack:
            print("\t", str(thing))
        print("\\end")
        last_end = input_start
        merge_length = 0
        for index in range(next_merge_stack_index):
            run = merge_stack[index]

            print(str(run), run.start, input_start)
            self.assertEqual(last_end, run.start)
            merge_length += run.end - run.start
            last_end = run.end

        self.assertEqual((input_end - input_start), merge_length)


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    our_peek_sorter = Sorter_Peeksort(input_list, k)
    our_peek_sorter.sort()


def run_all(input_list, k):
    all_fine = True

    for current_input in input_list:
        unsorted_input = current_input.copy()
        sort(current_input, k)

        if current_input != sorted(current_input):
            print("input: ", current_input, "wasn't sorted correctly!")
            print("output:", current_input)
            all_fine = False
        else:
            print("\n", unsorted_input, "sorts properly\n")

    if all_fine:
        print("test performed - it's all still working")

# todo: convert most of these into additional formal tests in test_sorter

# todo: testing required:
#       1. edge case: r_i is closer, but there's no dangly bit


# trivial, unsorted inputs
input_1 = [4, 3, 2, 1]
input_2 = [4, 3, 2, 1, 5, 7, 6, 8]
# fully sorted input
input_3 = [1, 2, 3, 4, 5, 6, 7, 8]

# reproducible random input
input_4 = list(range(10))
random.seed(12345678)
random.shuffle(input_4)

# edge case: long run in the middle of an input, with random stuff on either side (intended for use with k=2 and k=4)
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

all_sortable_inputs_k_equals_2 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8,
                                  input_11]
all_sortable_inputs_k_equals_3 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_4 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_5 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_6 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_7 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_8 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_9 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                  input_10, input_11, input_12]
all_sortable_inputs_k_equals_10 = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9,
                                   input_10, input_11, input_12]

# uncomment to check that all sortable inputs are still sorting correctly
# run_all(all_sortable_inputs_k_equals_2, 2)
# input()

# choose an input
our_input = input_9

print("sorting:", our_input)
sort(our_input, 2)
print("sorted: ", our_input)

if our_input == sorted(our_input):
    print("sorted correctly")
else:
    print("not sorted correctly")
