# todo - update to use new methods

import unittest
from Tests import Test_Sorters, Test_MergerIPQs, Test_Mergers

# wipe testing files to prevent leaks from earlier tests
Test_Mergers.Test_Mergers.clear_file_merger()


# gather all tests
suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQs.Test_MergerIPQs)]
comboSuite = unittest.TestSuite(suiteList)

# run them
unittest.TextTestRunner().run(comboSuite)
