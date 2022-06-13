from Merger_IPQs import MergerIPQ
from Mergers import Merger
from Sorters import Sorter
from Tests import Test
import os
import unittest
from typing import Union


class Test_Sorters_2(Test.Test):
    def __init__(self, sorter_init: type(Sorter.Sorter),
                 override_merger_init: Union[bool, type(Merger.Merger)] = False,
                 override_merger_ipq_init: Union[bool, type(MergerIPQ.MergerIPQ)] = False,
                 check_ipq_selection=False,
                 check_merger_selection=False):
        super().__init__(check_ipq_selection, check_merger_selection)

        self.sorter_init = sorter_init
        self.override_merger_init = override_merger_init
        self.override_merger_ipq_init = override_merger_ipq_init

    # * * * * * * ** * * * * * * *
    # * * * * * INPUTS * * * * * *
    # * * * * * * ** * * * * * * *

    def _sort_single_element(self):
        """tests that a sorter can handle the trivial input of a single character. note that this should NOT be special
        cased - the potential flaw we're checking for here is the creation of a merger for an input that doesn't need
        one"""
        random_input = [1]
        sorted_input = [1]
        sorter = self.sorter_init(random_input, 2,
                                  merger_ipq_init=None,
                                  merger_init=None,
                                  test_mode=True)
        sorter.sort()

        # check sortedness
        self.assertEqual(sorted_input, random_input)

        # assure that no mergers or merger ipqs are used for this input
        self.assertFalse(os.path.isfile("test_options_merger_ipq.txt")), "a merger ipq was used for a single element"
        self.assertFalse(os.path.isfile("test_options_merger.txt")), "a merger was used for a single element"

    # * * * * * * * * * * * * * *
    # * * * * * UTILITY * * * * *
    # * * * * * * * * * * * * * *

    # * * * * * * * * * * * * * *
    # * * * * * TESTS * * * * * *
    # * * * * * * * * * * * * * *

    # * * * * * *  * * * * * * *
    # * * * * * MAIN * * * * * *
    # * * * * * *  * * * * * * *

    # todo - why is this even necessary? if a test isn't copied in here, it says that it runs... but doesn't
    def runTest(self):
        pass


if __name__ == "__main__":
    unittest.main()

