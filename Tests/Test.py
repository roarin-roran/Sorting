import os
from os.path import exists
import unittest
from Support import ListSlice


class Test:
    def __init__(self, check_ipq_selection=False, check_merger_selection=False):
        self.check_ipq_selection = check_ipq_selection
        self.check_merger_selection = check_merger_selection

        self.test_case = None

        self.clear_unnecessary_files()

    def _check_correct_merger_ipq_used(self, correct_merger_ipq_init):
        """checks that the input is the only ipq used since records were last wiped"""
        blank_merger_ipq = correct_merger_ipq_init([])
        f_r = open("test_options_merger_ipq.txt", "r")

        correct_answer = str(blank_merger_ipq.option_code)

        for entry in f_r:
            given_answer = entry[0]
            self.test_case.assertEqual(correct_answer, given_answer)

        f_r.close()

    def _check_correct_merger_used(self, correct_merger_init):
        """checks that the correct merger is the only merger that's been used since the last wipe"""
        # blank merger must be created for its option code to be read
        # two runs must be passed for merger two way to work (but they can be empty)
        blank_merger = correct_merger_init([[], []], ListSlice.ListSlice([], 0, 0))
        f_r = open("test_options_merger.txt", "r")

        correct_answer = str(blank_merger.option_code)

        for entry in f_r:
            given_answer = entry[0]
            self.test_case.assertEqual(correct_answer, given_answer)

        f_r.close()

    def clear_unnecessary_files(self):
        if not self.check_ipq_selection:
            self.clear_file_ipq()
        if not self.check_merger_selection:
            self.clear_file_merger()

    @staticmethod
    def clear_all_files():
        Test.clear_file_ipq()
        Test.clear_file_merger()

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
        """prints all merger IPQs used since the last wipe"""
        if exists("test_options_merger_ipq.txt"):
            f_r = open("test_options_merger_ipq.txt", "r")
            for entry in f_r:
                print(entry)

            f_r.close()

    @staticmethod
    def print_options_merger():
        """prints all mergers used since the last wipe"""
        if exists("test_options_merger.txt"):
            f_r = open("test_options_merger.txt", "r")
            for entry in f_r:
                print(entry)

            f_r.close()
