from Sorters import Sorter
from Mergers import Merger_Adaptive
from Merger_IPQs import MergerIPQ_Dummy


# defines methods shared by sorters using ping pong memory management
class Sorter_PingPong(Sorter.Sorter):
    def __init__(self, input_array, k,
                 merger_ipq_init=MergerIPQ_Dummy.MergerIPQ_Dummy,
                 merger_init=Merger_Adaptive.Merger_Adaptive):
        # passes data down, where it'll be saved
        super().__init__(input_array, k, merger_ipq_init, merger_init)

        self.input_length = len(input_array)

        self.ping = input_array.copy()
        self.pong = input_array.copy()

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
