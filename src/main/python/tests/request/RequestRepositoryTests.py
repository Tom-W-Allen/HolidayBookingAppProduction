from unittest import TestCase
from HolidayBookingApp.domains.request.RequestRepository import RequestRepository
from HolidayBookingApp.tests.common.TestExecution import *
from HolidayBookingApp.tests.request.RequestTestData import *
from datetime import datetime, date

_connection_string = "persistence/HolidayBookingDatabase.db"
_class_under_test = "domains.request.RequestRepository"
_sut = RequestRepository(_connection_string)
_test_executor = TestExecutor(_sut, _class_under_test)
_current_date = datetime(date.today().year, date.today().month, date.today().day)


class RequestRepositoryMethodTests(TestCase):

    def test_create_request_id_set_to_1_when_no_other_requests_exist(self):
        test_data = test_create_request_id_set_to_1_when_no_other_requests_exist_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, "create_request")

    def test_create_request_id_incremented_by_1_when_other_requests_exist(self):
        test_data = test_create_request_id_incremented_by_1_when_other_requests_exist_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, "create_request")

    def test_get_requests_for_approval_returns_correct_results_when_requests_exist(self):
        test_data = test_get_requests_for_approval_returns_correct_results_when_requests_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_requests_for_approval")

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].id, actual_result[i].id)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(test_data.expected_result[i].status, actual_result[i].status)

    def test_get_requests_for_review_returns_correct_results_when_requests_exist(self):
        test_data = test_get_requests_for_review_returns_correct_results_when_requests_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_requests_for_approval")

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].id, actual_result[i].id)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(test_data.expected_result[i].status, actual_result[i].status)

    def test_approve_request_request_approved_when_method_called(self):

        test_data = test_approve_request_request_approved_when_method_called_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, "approve_request")

    def test_reject_request_request_rejected_when_method_called(self):

        test_data = test_reject_request_request_rejected_when_method_called_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, "reject_request")

    def test_cancel_request_request_cancelled_when_method_called(self):

        test_data = test_cancel_request_request_cancelled_when_method_called_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, "reject_request")

    def test_get_pending_holidays_holidays_total_returned_when_pending_holidays_exist(self):

        test_data = test_get_pending_holidays_holidays_total_returned_when_pending_holidays_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_pending_holidays")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_pending_holidays_holidays_0_returned_when_pending_holidays_do_not_exist(self):

        test_data = test_get_pending_holidays_holidays_0_returned_when_pending_holidays_do_not_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_pending_holidays")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_live_request_history_request_history_returned_when_requests_exist(self):

        test_data = test_get_live_request_history_request_history_returned_when_requests_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_live_request_history")

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].id, actual_result[i].id)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(test_data.expected_result[i].status, actual_result[i].status)

    def test_get_all_requests_by_status_requests_returned_when_requests_exist(self):

        test_data = test_get_all_requests_by_status_requests_returned_when_requests_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_all_requests_by_status")

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].id, actual_result[i].id)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].total_holidays, actual_result[i].total_holidays)
            self.assertEqual(test_data.expected_result[i].status, actual_result[i].status)
