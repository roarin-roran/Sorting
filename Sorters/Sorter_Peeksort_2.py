from Sorters import Sorter
from Support import ListSlice
import unittest
import random


class Sorter_Peeksort_2(Sorter.Sorter):
    """a full re-implementation of Sorter_Peeksort, addressing three issues:
        1. poor documentation throughout. it should be extremely clear what the algorithm is without reference to my
           notebooks. readability should also be improved by shrinking functions.
        2. inconsistent use of inclusive/exclusive conventions. multiple parts of the code generate runs which start and
           end at the same element - an impossibility with exclusive conventions.
        3. the base case was only ever intended to be temporary - identifying where the base case is reached and
           handling it should be substantially improved.

        Algorithm: https://bamboo.zulipchat.com/#narrow/stream/312930-powersort
    """

    def __init__(self, input_list, k,
                 merger_ipq_init=None,
                 merger_init=None,
                 test_mode=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

        # used for merging
        self.temp_list = [-1] * len(input_list)

        # defined globally to easily return from a function
        self.next_input_start = 0
        self.next_first_run_end = 0

    def sort(self):
        """sort the list using k way peeksort"""
        print("1. input:\t\t", self.input_list, "\n")

        # the right hand edge of the left hand run, with an exclusive convention
        first_run_end = self._extend_run_right(0, len(self.input_list))

        if first_run_end == len(self.input_list):
            print("input is already sorted!")
        else:
            # the left hand edge of the rightmost run, inclusively
            last_run_start = self._extend_run_left(len(self.input_list), 0)

            print("14. calling recursive sort from first position")
            self._recursively_sort(0, first_run_end, last_run_start, len(self.input_list))
            print("21. fin")

    def _extend_run_right(self, run_start, next_run_start):
        """takes the start of a run, and extends it towards where the run on the right starts.

        note that run_start and next_run_start are both run starts(inclusive), while r_i is a run end(exclusive)"""

        r_i = run_start
        while r_i < next_run_start - 1:
            if self.input_list[r_i + 1] >= self.input_list[r_i]:
                r_i += 1
            else:
                break

        return r_i + 1

    def _extend_run_left(self, run_end, previous_run_end):
        """takes a run end, m_i, and extends it towards where the run on the left ends.

        note that m_i and next_first_run_end are both run ends(exclusive) while l_i is a run start(inclusive)"""
        l_i = run_end - 1
        while l_i > previous_run_end:
            if self.input_list[l_i - 1] <= self.input_list[l_i]:
                l_i -= 1
            else:
                break

        return l_i

    def _recursively_sort(self, input_start, first_run_end, last_run_start, input_end):
        """splits each inserted section into up to k pieces, sorts them recursively, then merges them"""

        print("2. recursion begins: \t", self.input_list, input_start, first_run_end, last_run_start, input_end)
        # print("\t(start, first run, last run, end)")
        # print("\t(", input_start, first_run_end, last_run_start, input_end, ")")
        # print("\t", self.input_list[input_start:input_end])

        # define a merge stack - a list of objects which will be merged before this call is completed.
        # todo - check why this needs size k+2. document this
        # todo - future version should potentially use a global list to declare the whole thing at once.
        merge_stack = [ListSlice.ListSlice([0], 0, 1)] * (self.k + 2)
        next_merge_stack_index = 0

        # todo - test for a single run somewhere. old code does this here, possibly to save repetitions
        #   use list.is_sorted to test for sortedness, testing from the last character of the first run to the first
        #   character of the last run

        # step 1: detect trivial input, and handle it using a base case.
        print("12. detect trivial in:\t", self.input_list, input_start, first_run_end, last_run_start, input_end)
        if self._detect_trivial_input(input_start, first_run_end, last_run_start, input_end):
            print("10. before base case:\t", self.input_list, first_run_end, input_end)
            self._base_case(input_start, first_run_end, input_end)
            print("11. after base case:\t", self.input_list)
        else:
            # step 2: assuming nontrivial input, generate a list of values where the input may be split for recursion
            m = self._generate_initial_m_values(input_start, first_run_end, last_run_start, input_end)

            # step 3?: are there any split points which aren't in the first or last run?
            if len(m) > 0:
                # step 3a1: if there are any valid m values, initialise and begin a loop over them
                self.next_input_start = input_start
                self.next_first_run_end = first_run_end

                m_index = 0
                times_around = 0
                while m_index < len(m):
                    print("times around: ", times_around)
                    times_around += 1
                    # step 3a2: find the left edge of the run containing m_i
                    l_i = self._extend_run_left(m[m_index] + 1, self.next_first_run_end)

                    # step 3a3: find the rightmost edge of the run containing m_i
                    r_i = self._extend_run_right(m[m_index], last_run_start)

                    # print("\t\trun detected!", l_i, m[m_index], r_i)

                    # step 3a4: check for additional m values in the current run - these can safely be skipped.
                    m_values_to_skip = self._count_skipped_m_values(m, m_index, r_i)

                    # step 3a4?: are there any such values?
                    if m_values_to_skip:
                        print("7. handle case: overlap")
                        # print("handle case: overlap")
                        # step 3a4a1: skip overlapped m values
                        m_index += m_values_to_skip

                        # todo: test from here on

                        # step 3a4a2?: is there anything before this run (such as another run, or an unsorted portion)
                        if self.next_input_start < l_i:
                            # save this to use later
                            next_input_start_copy = self.next_input_start

                            # step 3a4a2a1: if there is an unsorted portion, recurse on it
                            if self.next_first_run_end < l_i:
                                print("15, calling recursive sort from the second position")
                                self._recursively_sort(self.next_input_start, self.next_first_run_end, l_i, l_i)

                            # step 3a4a2a2: now that everything before the run containing m_i is a single run, throw
                            # that run on the merge stack
                            self._add_to_merge_stack(next_input_start_copy, l_i, merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1

                        # step 3a4a3: throw the run containing m_i on the merge stack
                        self._add_to_merge_stack(l_i, r_i, merge_stack, next_merge_stack_index)
                        next_merge_stack_index += 1
                        self.next_input_start = r_i
                        self.next_first_run_end = r_i

                    else:
                        print("8. handle case: no overlap")

                        # step 3a4b?
                        # when there is no overlap, where the run goes depends on whether m_i is closer to l_i or r_i

                        # if m_i is closer to l_i
                        if m[m_index] - l_i <= r_i - m[m_index]:
                            # step 3a4ba: m_i closer to l_i
                            # if there's an unsorted portion, recurse on it and throw it on the merge stack
                            next_input_start_copy = self.next_input_start
                            if self.next_first_run_end < l_i:
                                # end is l_i+1 because ends are exclusive
                                print("16, calling recursive sort from the third position")
                                self._recursively_sort(self.next_input_start, self.next_first_run_end, l_i, l_i)
                            self._add_to_merge_stack(next_input_start_copy, l_i,
                                                     merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1

                            # this run defines the start of the new dangly bit
                            self.next_input_start = l_i
                            self.next_first_run_end = r_i
                        else:
                            # step 3a4bb: m_i closer to r_i
                            # recurse on the whole thing - including the run containing m_i
                            next_input_start_copy = self.next_input_start
                            if self.next_input_start < l_i:
                                print("17, calling recursive sort from the fourth position")
                                self._recursively_sort(next_input_start_copy, self.next_first_run_end, l_i, r_i)

                            # there always must be a run, even if it's just a single character.
                            self._add_to_merge_stack(next_input_start_copy, r_i, merge_stack, next_merge_stack_index)
                            next_merge_stack_index += 1

                            # the next dangly bit starts without a run.
                            self.next_input_start = r_i
                            self.next_first_run_end = r_i

                    m_index += 1
                    print("23. trying m value", m_index, "from", m)

                    # step 3a5? handle the last non-run section, and the final run.
                    # step 3a5a. if there's a non-run before the last run, recurse on the last section
                    if self.next_input_start < last_run_start:
                        print("6. end handling, case 1")
                        next_input_start_copy = self.next_input_start
                        print("18, calling recursive sort from the fifth position")
                        self._recursively_sort(self.next_input_start, self.next_first_run_end, last_run_start,
                                               input_end)
                        self._add_to_merge_stack(next_input_start_copy, input_end, merge_stack, next_merge_stack_index)
                        next_merge_stack_index += 1
                    # step 3a5b if there's not, but there is a run - throw it on the merge stack
                    elif last_run_start < input_end:
                        print("7. end handling, case 2")
                        self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
                        next_merge_stack_index += 1
                    # if neither is true, no action is required.
            else:
                # step 3b: no valid m values exist
                print("9. handle case where no valid m values exist")

                # step 3b? is the first run longer than the second run?
                if (first_run_end - input_start) > (input_end - last_run_start):
                    # step 3ba. if the first run is longer, throw it on the stack and recurse on everything else.
                    self._add_to_merge_stack(input_start, first_run_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1
                    print("19, calling recursive sort from the sixth position")
                    self._recursively_sort(first_run_end, first_run_end, last_run_start, input_end)
                    self._add_to_merge_stack(first_run_end, input_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1

                else:
                    # step 3bb. if the second run is longer, throw it on the stack and recurse on everything else.
                    print("20, calling recursive sort from the seventh position")
                    self._recursively_sort(input_start, first_run_end, last_run_start, last_run_start)
                    self._add_to_merge_stack(first_run_end, last_run_start, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1

                    self._add_to_merge_stack(last_run_start, input_end, merge_stack, next_merge_stack_index)
                    next_merge_stack_index += 1

            # step 4: merge.
            # if there are multiple things on the merge stack - merge them, if not this step is effectively done
            if next_merge_stack_index > 1:

                # print("issue seems to be at merge time - check from here")
                print("3. before merge: \t\t", self.input_list, input_start, input_end, merge_stack, next_merge_stack_index)
                self._merge(input_start, input_end, merge_stack, next_merge_stack_index)
                print("4. after merge: \t\t", self.input_list, input_start, input_end, merge_stack, next_merge_stack_index)

        print("13. recursion ends")
        # print("end of recursive step:", self.input_list[input_start:input_end])


    def _base_case(self, input_start, first_run_end, input_end):
        """a low-overhead way to sort small inputs, used for the bottom of the tree. insertion sort, starting with the
        first run is used"""

        # for all unsorted elements in the desired range
        for i in range(first_run_end, input_end):
            # copy out an element
            key = self.input_list[i]

            # while it's out of order, move a space towards the appropriate position in the input
            j = i - 1
            while j >= input_start and key < self.input_list[j]:
                self.input_list[j + 1] = self.input_list[j]
                j = j - 1

            # fill that space with the desired element
            self.input_list[j + 1] = key

    def _detect_trivial_input(self, input_start, first_run_end, last_run_start, input_end):
        """an easily tweakable/overridable test for trivial input which should be handled by the bast case """

        # todo - optimise this method, ensuring that it always meets its safety criteria and is appropriately agressive
        #   should this include the case where there are no m values?

        return input_end - first_run_end <= self.k

    def _generate_initial_m_values(self, input_start, first_run_end, last_run_start, input_end):
        """generates an array of k-1 m values (places where the input would naturally be split in order to give k lists
        on which to recurse).

        returns only those which are in between the first and last run

        uses an inclusive notation: [4,3,2,1] having an m value of 2 will split the input into [4,3] and [2,1]"""

        # the gap between m values
        step = (input_end - input_start) / self.k

        # work out how many m values are inside the first run without declaring any memory
        trim_from_front = 0
        i = 0
        while i < self.k - 1:
            current_index = input_start + round(step * (i + 1))
            if current_index <= first_run_end:
                trim_from_front += 1
            else:
                break

            i += 1

        # repeat for the last run
        trim_from_back = 0
        i = self.k - 2
        while i >= trim_from_front:
            current_index = input_start + round(step * (i + 1))
            if current_index > last_run_start:
                trim_from_back += 1
            else:
                break

            i -= 1

        # using trim_from_from and trim_from_back create a list of m values
        m = [-1] * (self.k - 1 - trim_from_front - trim_from_back)
        j = 0
        for i in range(trim_from_front, self.k - 1 - trim_from_back):
            m[j] = input_start + round(step * (i + 1))
            j += 1

        return m

    @staticmethod
    def _count_skipped_m_values(m, m_index, r_i):
        """when a run is extended right, it may overlap with other m values (run creation/splitting points).

        count how many are overlapped, to skip them."""
        m_values_to_skip = 0
        # for all m values after the current one.
        for j in range(m_index + 1, len(m)):
            if m[j] <= r_i:
                m_values_to_skip += 1
            else:
                break

        return m_values_to_skip

    def _add_to_merge_stack(self, run_start, run_end, merge_stack, next_merge_stack_index):
        """adds a single, sorted run to the merge stack, ensuring no formatting mistakes."""
        print("22. add to merge stack: ", run_start, run_end)
        merge_stack[next_merge_stack_index] = ListSlice.ListSlice(self.input_list, run_start, run_end)

    def _merge(self, input_start, input_end, merge_stack, next_merge_stack_index):
        # todo - test me
        # todo - update to generate runs in a memory efficient way, rendering the slice unnecesary

        print("printing perge stack:")
        for i in merge_stack[:next_merge_stack_index]:
            print("\t", i)

        our_merger = self.merger_init(merge_stack[:next_merge_stack_index],
                                      ListSlice.ListSlice(self.temp_list, input_start, input_end),
                                      test_mode=self.test_mode)
        our_merger.merge()

        # note that this step is inefficient, and improving it is listed as issue #68 on github.
        for index in range(input_start, input_end):
            self.input_list[index] = self.temp_list[index]




class Peeksort_Tester(unittest.TestCase):
    def test_m_generation(self):
        i_o_pairs = []

        # format:
        # list, start, first run, last run, end, k, correct answer
        i_o_pairs.append([[8, 7, 6, 5, 4, 3, 2, 1], 0, 1, 7, 8, 4, [2, 4, 6]])
        i_o_pairs.append([[9, 8, 7, 6, 5, 4, 3, 2, 1], 0, 1, 8, 9, 3, [3, 6]])
        i_o_pairs.append([[5, 4, 3, 2, 1], 0, 1, 4, 5, 2, [2]])
        # testing front run exclusion
        i_o_pairs.append([[1, 8, 7, 6, 5, 4, 3, 2], 0, 2, 7, 8, 4, [4, 6]])
        i_o_pairs.append([[1, 2, 3, 8, 7, 6, 5, 4], 0, 4, 7, 8, 4, [6]])
        i_o_pairs.append([[1, 2, 3, 4, 5, 8, 7, 6], 0, 6, 7, 8, 4, []])
        # testing final run exculsion
        # todo - consider removing another m value in these edge cases. if it doesn't create a merge balancing issue,
        #  it saves work
        i_o_pairs.append([[8, 7, 6, 5, 4, 3, 1, 2], 0, 1, 6, 8, 4, [2, 4, 6]])
        i_o_pairs.append([[8, 7, 6, 5, 1, 2, 3, 4], 0, 1, 4, 8, 4, [2, 4]])
        i_o_pairs.append([[8, 7, 1, 2, 3, 4, 5, 6], 0, 1, 2, 8, 4, [2]])

        test_case_counter = 1
        for pair in i_o_pairs:
            our_peek_sorter = Sorter_Peeksort_2(pair[0], pair[5])
            m = our_peek_sorter._generate_initial_m_values(pair[1], pair[2], pair[3], pair[4])
            # print("test", test_case_counter)
            test_case_counter += 1
            self.assertEqual(pair[6], m)
            # print("pass")


def run_test_cases():
    # todo - move me to the appropriate place (probably these are good test cases for all sorters)
    # trivial, unsorted inputs
    input_1 = [4, 3, 2, 1]
    input_2 = [4, 3, 2, 1, 5, 7, 6, 8]
    # fully sorted input
    input_3 = [1, 2, 3, 4, 5, 6, 7, 8]

    # reproducible random input
    input_4 = list(range(11))
    random.seed(12345678)
    random.shuffle(input_4)

    all_inputs = [input_1, input_2, input_3, input_4]

    case_counter = 1
    for case in all_inputs:
        print("sorting case", case_counter)
        case_counter += 1

        sort(case, k=3)

        print()
        print(case)

        print()
        print("- - - - - - - - - - - - - -")
        print()


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    our_peek_sorter = Sorter_Peeksort_2(input_list, k)
    our_peek_sorter.sort()


run_test_cases()

if __name__ == "__main__":
    unittest.main()


# next thing: setup a propper test mode with print statements, catch where duplicate elements are enterring
