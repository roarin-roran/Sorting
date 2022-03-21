import unittest
from Tests import Test_Mergers, Test_MergerIPQ, Test_Sorters

suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQ.Test_MergerIPQ)]

comboSuite = unittest.TestSuite(suiteList)
unittest.TextTestRunner().run(comboSuite)
