from abc import ABC
from Sorters import Sorter


class Sorter_PingPong(Sorter.Sorter, ABC):
    """a middle class between the Sorter class, and fully implemented sorters which use ping pong memory management.
    sets up various shared objects, variables, and methods"""
    def __init__(self, input_list, k,
                 merger_ipq_init=None,
                 merger_init=None,
                 test_mode=False):
        # passes data down, where it'll be saved
        super().__init__(input_list, k, merger_ipq_init, merger_init, test_mode)

        self.input_length = len(input_list)

        self.ping = input_list
        self.pong = input_list.copy()

        self.read_ping_write_pong = True

    # read and write lists change - returns the internal list being read from
    def _get_read_list(self):
        if self.read_ping_write_pong:
            return self.ping
        else:
            return self.pong

    # read and write list change - returns the internal list being written to
    def _get_write_list(self):
        if self.read_ping_write_pong:
            return self.pong
        else:
            return self.ping
