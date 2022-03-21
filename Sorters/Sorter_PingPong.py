from abc import ABC
from Sorters import Sorter


# defines methods shared by sorters using ping pong memory management
class Sorter_PingPong(Sorter.Sorter, ABC):
    def __init__(self, input_list, k,
                 merger_ipq_init=False,
                 merger_init=False):
        # passes data down, where it'll be saved
        super().__init__(input_list, k, merger_ipq_init, merger_init)

        self.input_length = len(input_list)

        self.ping = input_list
        self.pong = input_list.copy()

        self.read_ping_write_pong = True

    # read and write lists change - returns the internal list being read from
    def get_read_list(self):
        if self.read_ping_write_pong:
            return self.ping
        else:
            return self.pong

    # read and write list change - returns the internal list being written to
    def get_write_list(self):
        if self.read_ping_write_pong:
            return self.pong
        else:
            return self.ping
