# todo - update to use new methods

import unittest
from Tests import Test_MergerIPQs, Test_Mergers, Test_Sorters

# wipe testing files to prevent leaks from earlier tests
Test_Mergers.Test_Mergers.clear_file_merger()


# gather all tests
suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.TestCases),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.TestCases),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQs.TestCases)]
comboSuite = unittest.TestSuite(suiteList)

# run them
unittest.TextTestRunner().run(comboSuite)
