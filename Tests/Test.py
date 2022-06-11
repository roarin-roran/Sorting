import os
from os.path import exists
import unittest


class Test(unittest.TestCase):
    def __init__(self,
                 check_ipq_selection=False,
                 check_merger_selection=False):
        super().__init__()

        if not check_ipq_selection:
            self.clear_file_ipq()
        if not check_merger_selection:
            self.clear_file_merger()

        self.check_ipq_selection = check_ipq_selection
        self.check_merger_selection = check_merger_selection

    def clear_unnecessary_files(self):
        if not self.check_ipq_selection:
            self.clear_file_ipq()
        if not self.check_merger_selection:
            self.clear_file_merger()

    @staticmethod
    def clear_file_ipq():
        """wipes the options file"""
        if exists("test_options_merger_ipq.txt"):
            os.remove("test_options_merger_ipq.txt")

    @staticmethod
    def clear_file_merger():
        """wipes the file which records which mergers have been used"""
        if exists("test_options_merger.txt"):
            os.remove("test_options_merger.txt")

    @staticmethod
    def print_options_merger_ipq():
        """print the record file, to see which ipqs have been used since the last wipe"""
        if exists("test_options_merger_ipq.txt"):
            f_r = open("test_options_merger_ipq.txt", "r")
            for entry in f_r:
                print(entry)
