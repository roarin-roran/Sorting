from Sorters import Sorter_PingPong
from Support import ListSlice
import math


class Sorter_PingPong_BottomUp(Sorter_PingPong.Sorter_PingPong):
    """a ping-pong implementation of a bottom-up k-way merge sort with no run detection"""
    def __init__(self, input_list, k,
                 merger_ipq_init=None,
                 merger_init=None,
                 test_mode=False):

        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

        self.sorted = False

    def sort(self):
        """sorts the input using k elements without run detection"""
        run_length = 1

        # while the array isn't sorted
        while run_length < self.input_length:
            read_list = self._get_read_list()

            # a block consists of k runs, and is merged in a single step
            number_of_blocks = math.ceil(self.input_length / (self.k * run_length))
            for block_number in range(number_of_blocks):
                runs = []
                # initialise run_start - run end doesn't need initialising
                run_start = block_number * run_length * self.k

                # if there's only going to be one run in this block, just copy the run from the read list to the write
                # list
                if run_start + run_length >= self.input_length:
                    write_list = self._get_write_list()

                    posn = run_start
                    while posn < self.input_length:

                        write_list[posn] = read_list[posn]

                        posn += 1

                    break

                for run in range(self.k):
                    run_end = min(run_start + run_length, self.input_length)
                    runs.append(ListSlice.ListSlice(read_list, run_start, run_end))

                    run_start += run_length

                    # don't add nonsense runs when you run out of stuff to put in them
                    if run_start >= self.input_length:
                        break

                write_list_slice = ListSlice.ListSlice(self._get_write_list(), runs[0].start, runs[-1].end)

                # merge, using an external merger object
                our_merger = self.merger_init(runs, write_list_slice,
                                              merger_ipq_init=self.merger_ipq_init,
                                              test_mode=self.test_mode)
                our_merger.merge()

                # swap the ping and pong arrays
            self.read_ping_write_pong = not self.read_ping_write_pong

            run_length *= self.k

        # copy the correct answer back into the input list if these lists differ
        read_list = self._get_read_list()
        if read_list != self.input_list:
            for i in range(len(self.input_list)):
                self.input_list[i] = read_list[i]

        return self.input_list


# sorts the input
def sort(input_list, k=2):
    """creates a sorter object and calls the sort method"""
    sorter = Sorter_PingPong_BottomUp(input_list, k)
    sorter.sort()
