from Sorters import Sorter
from Support import ListSlice
import random
from Mergers import Merger_Tester
from Merger_IPQs import MergerIPQ_Dummy


# todo: document conventions used wrt inclusive or exclusive parts of the list in function parameters
class Sorter_Peeksort(Sorter.Sorter):
    def __init__(self, input_list, k,
                 merger_ipq_init=False,
                 merger_init=False,
                 test_mode=False):
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

    def sort(self):
        """put the list in sorted order using k way peeksort"""

        first_run_end = self._extend_run_right(0, len(self.input_list))
        last_run_start = self._extend_run_left(len(self.input_list) - 1, first_run_end)

        self._recursively_sort(0, first_run_end, last_run_start, len(self.input_list))

    # sorts the input
    def _recursively_sort(self, input_start, first_run_end, last_run_start, input_end):
        """recursively sort an input assumed to contain at least two runs"""
        # todo - test for one big run as a step 0, and strip out higher level tests. this will make things shorter and
        #  more readable

        # 1. test for and handle inputs with at most k inputs that aren't in known runs.
        #   (note that inputs where the first run overlaps the second are illegal)
        if last_run_start - first_run_end <= self.k:
            self._handle_trivial_input(input_start, first_run_end, last_run_start, input_end)
        else:
            # find all m values outside of a known run, steps 2 and 3
            m = self._generate_initial_m_values(first_run_end, last_run_start)

            # 6. initialise the dangling end
            next_input_start = input_start
            next_first_run_end = first_run_end

            # 4. generate recursive calls and merges using these m values
            print("\nm:", m, "\n")

            i = 0
            while i < len(m):
                print("\tm_i:       ", m[i])

                # 5. find the left edge of the run (extend run left)
                l_i = self._extend_run_left(m[i], next_first_run_end)
                print("\tl_i:       ", l_i)

                # note that step 6 has been moved, and a rewrite is required because this is kinda confusing.

                # 7. find the rightmost edge of the run (extend run right)
                r_i = self._extend_run_right(m[i], last_run_start)
                print("\tr_i:       ", r_i)

                # todo - do this with a function that returns the value to add to i for neatness
                # 8. if any other m_i values are in this run: discard them, recurse on the dangly bit, merge the run
                m_values_to_skip = 0
                # for all m values after the current one.
                for j in range(i + 1, len(m)):
                    if m[j] < r_i:
                        m_values_to_skip += 1
                    else:
                        break

                if m_values_to_skip:
                    print("\n\tskipping", m_values_to_skip, "m values, because they're contained in this run.")
                    # increment i to skip the runs
                    i += m_values_to_skip

                    # if there's anything to recurse on
                    if next_input_start < l_i:
                        # recurse on the dangly bit (if it isn't just a run) and throw it on the merge stack
                        if next_first_run_end < l_i:
                            print("\t\trecurse on:", next_input_start, next_first_run_end, l_i, l_i+1)
                        print("\t\tmerge:     ", next_input_start, l_i + 1)
                    # throw the discovered run on the merge stack
                    print("\t\tmerge:     ", l_i, r_i)
                    next_input_start = r_i - 1
                    next_first_run_end = r_i
                # 9. if not, it depends on whether m_i is closer to l_i or r_i
                else:
                    if m[i] - l_i <= r_i - m[i]:
                        print("\tl_i is closer(default)")
                        # recurse on the dangly bit (if it isn't just a run) and throw it on the merge stack
                        if next_first_run_end < l_i:
                            # end is l_i+1 because ends are exclusive
                            print("\t\trecurse on:", next_input_start, next_first_run_end, l_i, l_i + 1)
                        print("\t\tmerge:     ", next_input_start, l_i + 1)

                        # this run defines the start of the new dangly bit
                        next_input_start = l_i
                        next_first_run_end = r_i
                    else:
                        print("\tr_i is closer")
                        # todo: see test 3 below (r_i without a dangly bit)
                        # recurse on both the dangly bit and the new run (there should always be a dangly bit)
                        print("\t\trecurse on:", next_input_start, next_first_run_end, l_i, r_i)
                        print("\t\tmerge:     ", next_input_start, r_i)

                        # the next dangly bit start without a run.
                        # -1 to fix convention
                        next_input_start = r_i - 1
                        next_first_run_end = r_i

                print("\tnext peek time!\n")
                i += 1

            # 10. handle the last non-run section, and the final run.
            print("\t handle last section")
            # if there's a non-run before the last run, recurse on the last section
            if next_input_start < last_run_start:
                print("\t\trecurse on:", next_input_start, next_first_run_end, last_run_start, input_end)
                print("\t\tmerge:     ", next_input_start, input_end)
            # if there's not, but there is a run - throw it on the merge stack
            elif last_run_start < input_end:
                print("\t\tmerge:     ", last_run_start, input_end)
            # if neither is true, no action is required.

            print("time to merge the merge stack!\n")

        # return when everything that was passed in is a single run
        return

    def _handle_trivial_input(self, input_start, first_run_end, last_run_start, input_end):
        print("_handle_trivial_input called")
        print("this method is currently broken as all hell - trust nothing south of here")

        print()
        print(self.input_list)
        print(input_start, first_run_end)

        # set the first element, while also building a list of the correct length and element type
        first_run = ListSlice.ListSlice(self.input_list, input_start, first_run_end)
        print(str(first_run))
        runs = [first_run] * (2 + (last_run_start - first_run_end))

        print(len(runs))

        # add middle elements, if any
        for index in range(first_run_end, last_run_start):
            runs[index] = ListSlice.ListSlice(self.input_list, index, index + 1)
            print("BOOYA")

        if last_run_start != input_end:
            # add the final run, if it exists
            runs[-1] = ListSlice.ListSlice(self.input_list, last_run_start, input_end)
            print(str(runs[-1]))


        print("input to merger:")
        runs_str = ""
        print(len(runs))
        for run in runs:
            runs_str += str(run)
        print(runs_str)
        print(input_start, input_end)

        output_list = [1, 2, 3, 4, 6, 7, 8, 5]
        print("before:", output_list)
        print("input before:", self.input_list)
        print()

        #findme
        our_merger = self.merger_init(runs, ListSlice.ListSlice(output_list, input_start, input_end))
        our_merger.merge()

        print("after: ", output_list)
        print("input after: ", self.input_list)
        print()


    # todo - write this without a list slice for cheaper memory interactions
    #   (try reducing the length of m at the beginning, then generating m_i values)
    def _generate_initial_m_values(self, first_run_end, last_run_start):
        # 2. create k-1 evenly spaced m_i values
        m = [0] * (self.k - 1)
        step = len(self.input_list) / self.k

        for i in range(self.k - 1):
            m[i] = round(step * (i + 1))

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

        # add one because r_i is exclusive
        return r_i + 1


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    our_peek_sorter = Sorter_Peeksort(input_list, k)
    our_peek_sorter.sort()


# todo: convert most of these into additional formal tests in test_sorter

# todo: testing required:
#       1. implement the merge stack, and automatically test that everything is merged exactly once.
#       2. edge case: all sorted bar one element at one end (for safety, make two such cases)
#       3. edge case: r_i is closer, but there's no dangly bit

# trivial, unsorted inputs
input_1 = [4, 3, 2, 1]
input_2 = [4, 3, 2, 1, 5, 7, 6, 8]
# fully sorted input
input_3 = [1, 2, 3, 4, 5, 6, 7, 8]

# reproducible random input
input_4 = list(range(24))
random.seed(12345678)
random.shuffle(input_4)

# edge case: long run in the middle of an input, with random stuff on either side (intended for use with k=2 and k=4)
input_5 = [4, 2, 3, 1, 5, 6, 7, 8, 11, 12, 10, 9]

# edge case: mostly sorted inputs, with one unsorted character on the left or right
input_6 = [5, 1, 2, 3, 4, 6, 7, 8]
# todo: fix, this case is broken (implying issues with _handle_trivial_cases). output: [1, 1, 1, 1, 1, 1, 1, 1]
input_7 = [1, 2, 3, 4, 6, 7, 8, 5]


# choose an input
our_input = input_7

print("sorting:", our_input)
sort(our_input, 4)
print("sorted: ", our_input)
