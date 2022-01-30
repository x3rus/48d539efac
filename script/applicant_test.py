#!/usr/bin/python
#
# Author: Thomas Boutry <thomas.boutry@x3rus.com>
##################################################

import applicant
import unittest
from unittest import mock


# This method will be used by the mock to replace requests.get
def mocked_requests_get_list_clients(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.content = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://fakeurl.com/api/v1/client':
        return MockResponse([], 200)
    elif args[0] == 'http://fakeurl-populated.com/api/v1/client':
        return MockResponse([{"id": "1234", "name": "first client", "url": "http://google.com"},
                            {"id": "9876", "name": "second client", "url": "http://yahoo.com"}], 200)
    elif args[0] == 'http://fakeurl-dberror.com/api/v1/client':
        return MockResponse({"error": "unable db connection"}, 500)

    return MockResponse(None, 404)


class applicantTest(unittest.TestCase):
    """unittest for applicant"""

    def test_loadingCsvFile(self):
        """ test loading csv file"""
        # pylint: disable=W

        use_cases = [
            {"csv_file": "./test/badFileName.csv", "len_clients": 0},
            {"csv_file": "./test/clients-2-load.csv", "len_clients": 4, "second_client_name": "second client"}
        ]

        app = applicant.applicant("https://fakeurl.com/api", "v1")

        for case in use_cases:
            clients_retreived = app.extractClientFromCsv(case['csv_file'])
            self.assertEqual(len(clients_retreived), case['len_clients'], "number of clients loaded")

            if len(clients_retreived) > 2:
                self.assertEqual(clients_retreived[1][1], case['second_client_name'], "Name of the second client")

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get_list_clients)
    def test_getClientList(self, mock_get):
        """ validate getting client list"""
        # pylint: disable=W
        use_cases = [
            # URL with no client in the database
            {"app_url": "http://fakeurl.com/api", "status_code": 200, "len_clients": 0},
            # URL with a few clients in the database
            {"app_url": "http://fakeurl-populated.com/api", "status_code": 200, "len_clients": 2,
             "second_client_name": "second client"},
            # URL with an error with the backend
            {"app_url": "http://fakeurl-dberror.com/api", "status_code": 500, "len_clients": 0},
        ]

        for case in use_cases:
            app = applicant.applicant(case["app_url"], "v1")
            r_code, clients_retreived = app.getClientList()

            self.assertEqual(len(clients_retreived), case['len_clients'], "number of clients loaded")

            if len(clients_retreived) > 2:
                self.assertEqual(clients_retreived[1]["name"], case['second_client_name'], "Name of the second client")

            self.assertEqual(r_code, case["status_code"], "http return code")


if __name__ == '__main__':
    unittest.main()
