import unittest
from Tests import Test_Mergers, Test_MergerIPQ, Test_Sorters

# gather all tests
suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQ.Test_MergerIPQ)]
comboSuite = unittest.TestSuite(suiteList)

# run them
unittest.TextTestRunner().run(comboSuite)
