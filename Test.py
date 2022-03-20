import unittest
import Test_Sorters
import Test_Mergers
import Test_MergerIPQ

suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQ.Test_MergerIPQ)]

comboSuite = unittest.TestSuite(suiteList)
unittest.TextTestRunner().run(comboSuite)


