#!/usr/bin/python
#
# Author: Thomas Boutry <thomas.boutry@x3rus.com>
##################################################

import applicant
import unittest


class applicantTest(unittest.TestCase):
    """unittest for applicant"""

    def test_loadingCsvFile(self):
        """ test loading csv file"""
        # pylint: disable=W

        use_cases = [
            {"csv_file": "./test/badFileName.csv", "len_clients": 0},
            {"csv_file": "./test/clients-2-load.csv", "len_clients": 4}
        ]

        app = applicant.applicant("https://fakeurl.com/api", "v1")

        for case in use_cases:
            clients_retreived = app.extractClientFromCsv(case['csv_file'])
            self.assertEqual(len(clients_retreived), case['len_clients'], "number of clients loaded")


if __name__ == '__main__':
    unittest.main()
