from Merger_IPQs import MergerIPQ_Dummy
from Codes import Code_IPQ


class MergerIPQ_Tester(MergerIPQ_Dummy.MergerIPQ_Dummy):
    """a re-skin of the Dummy IPQ used to test whether variables are passed correctly"""
    def __init__(self, initial_priorities, test_mode=True):
        super().__init__(initial_priorities, test_mode=test_mode, option_code=Code_IPQ.Code_Ipq.TESTER)
