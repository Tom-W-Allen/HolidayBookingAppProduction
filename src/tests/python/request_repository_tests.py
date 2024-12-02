from unittest import TestCase
from unittest.mock import patch

from domains.request.RequestRepository import RequestRepository
from data.RequestTestData import *
from datetime import datetime
from domains.request.models.Request import Request
from persistence.Database import Database

class RequestRepositoryMethodTests(TestCase):

    @patch.object(Database, "query_database", test_1_query_function)
    def test_create_request_id_set_to_1_when_no_other_requests_exist(self):
        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_1_method_parameters()

        sut.create_request(*input_parameters)

    @patch.object(Database, "query_database", test_2_query_function)
    def test_create_request_id_incremented_by_1_when_other_requests_exist(self):
        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_2_method_parameters()

        sut.create_request(*input_parameters)

    @patch.object(Database, "query_database", test_3_query_function)
    def test_get_requests_for_approval_returns_correct_results_when_requests_exist(self):
        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_3_method_parameters()

        expected_result = [Request(10,
                                   "Test Name",
                                   "Test Surname",
                                   datetime(2020, 5, 10),
                                   datetime(2020, 5, 15),
                                   5,
                                   "pending"),
                           Request(11,
                                   "Test Name",
                                   "Test Surname",
                                   datetime(2020, 6, 10),
                                   datetime(2020, 6, 16),
                                   6,
                                   "pending")
                           ]
        actual_result = sut.get_requests_for_approval(*input_parameters)

        self.assertEqual(len(expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].id, actual_result[i].id)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(expected_result[i].status, actual_result[i].status)

    @patch.object(Database, "query_database", test_4_query_function)
    def test_get_requests_for_review_returns_correct_results_when_requests_exist(self):
        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_4_method_parameters()

        expected_result = [Request(10,
                                   "Test Name",
                                   "Test Surname",
                                   datetime(2020, 7, 10),
                                   datetime(2020, 7, 15),
                                   5,
                                   "pending"),
                           Request(11,
                                   "Test Name",
                                   "Test Surname",
                                   datetime(2020, 8, 10),
                                   datetime(2020, 8, 16),
                                   6,
                                   "approved")
                           ]
        actual_result = sut.get_requests_for_review(*input_parameters)

        self.assertEqual(len(expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].id, actual_result[i].id)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(expected_result[i].status, actual_result[i].status)

    @patch.object(Database, "query_database", test_5_query_function)
    def test_approve_request_request_approved_when_method_called(self):
        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_5_method_parameters()

        sut.approve_request(*input_parameters)

    @patch.object(Database, "query_database", test_6_query_function)
    def test_reject_request_request_rejected_when_method_called(self):
        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_6_method_parameters()

        sut.reject_request(*input_parameters)

    @patch.object(Database, "query_database", test_7_query_function)
    def test_cancel_request_request_cancelled_when_method_called(self):

        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_7_method_parameters()

        sut.cancel_request(*input_parameters)

    @patch.object(Database, "query_database", test_8_query_function)
    def test_get_pending_holidays_holidays_total_returned_when_pending_holidays_exist(self):

        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_8_method_parameters()

        expected_result = 20
        actual_result = sut.get_pending_holidays(*input_parameters)

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_9_query_function)
    def test_get_pending_holidays_holidays_0_returned_when_pending_holidays_do_not_exist(self):

        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_9_method_parameters()

        expected_result = 0
        actual_result = sut.get_pending_holidays(*input_parameters)

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_10_query_function)
    def test_get_live_request_history_request_history_returned_when_requests_exist(self):

        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_10_method_parameters()

        expected_result = [Request(1,
                                   "",
                                   "",
                                   datetime(2020, 3, 10),
                                   datetime(2020, 3, 12),
                                   0,
                                   "pending"),
                           Request(2,
                                   "",
                                   "",
                                   datetime(2019, 3, 10),
                                   datetime(2019, 3, 12),
                                   0,
                                   "approved")
                           ]
        actual_result = sut.get_live_request_history(*input_parameters)

        self.assertEqual(len(expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].id, actual_result[i].id)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(expected_result[i].status, actual_result[i].status)

    @patch.object(Database, "query_database", test_11_query_function)
    def test_get_all_requests_by_status_requests_returned_when_requests_exist(self):

        mock_database = Database()
        sut = RequestRepository(mock_database)
        input_parameters = test_11_method_parameters()

        expected_result = [Request(1,
                                   "",
                                   "",
                                   datetime(2021, 3, 10),
                                   datetime(2021, 3, 12),
                                   0,
                                   "pending"),
                           Request(2,
                                   "",
                                   "",
                                   datetime(2020, 3, 10),
                                   datetime(2020, 3, 12),
                                   0,
                                   "pending")
                           ]

        actual_result = sut.get_all_requests_by_status(*input_parameters)

        self.assertEqual(len(expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].id, actual_result[i].id)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(expected_result[i].status, actual_result[i].status)