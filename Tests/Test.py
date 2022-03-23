import unittest
from Tests import Test_Mergers, Test_MergerIPQ, Test_Sorters

suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQ.Test_MergerIPQ)]

Test_Mergers.Test_Mergers.clear_file_merger()
Test_MergerIPQ.Test_MergerIPQ.clear_file_ipq()

comboSuite = unittest.TestSuite(suiteList)
unittest.TextTestRunner().run(comboSuite)
