import unittest
from Tests import Test_Mergers, Test_MergerIPQ, Test_Sorters
from os.path import exists
import os

# these should both be deleted by testing, but if a bug prevents their deletion, they can cause overflow errors -
# delete for safety
if exists("test_options_merger_ipq.txt"):
    os.remove("test_options_merger_ipq.txt")

if exists("test_options_merger.txt"):
    os.remove("test_options_merger.txt")

suiteList = [unittest.TestLoader().loadTestsFromTestCase(Test_Sorters.Test_Sorters),
             unittest.TestLoader().loadTestsFromTestCase(Test_Mergers.Test_Mergers),
             unittest.TestLoader().loadTestsFromTestCase(Test_MergerIPQ.Test_MergerIPQ)]

comboSuite = unittest.TestSuite(suiteList)
unittest.TextTestRunner().run(comboSuite)
