import unittest
from Tests import Test_Mergers, Test_MergerIPQ, Test_Sorters

# wipe testing files to prevent leaks from earlier tests
Test_Mergers.Test_Mergers.clear_file_merger()
Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

# gather all tests
suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQ.Test_MergerIPQ)]
comboSuite = unittest.TestSuite(suiteList)

# run them
unittest.TextTestRunner().run(comboSuite)
