from Sorters import Sorter

class Sorter_Peeksort(Sorter.Sorter):
    """a sorter using the munro and wild developed peeksort, extended to include k-way merging.

    a full rewrite of the older methds, using the algorithm published in my 2025 thesis."""

    def __init__(self, input_list, k,
                 verbose=False,
                 test_mode=False):
        # used for merging
        self.temp_list = [-1]*len(input_list)

        def sort(self):
            """high level method - sorts the input list, handling the initial setup (lines 1-10)"""
            pass

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

# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    our_peek_sorter = Sorter_Peeksort(input_list, k)
    our_peek_sorter.sort()

#def say_hi():
print("hi")