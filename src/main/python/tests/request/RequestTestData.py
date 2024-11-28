from HolidayBookingApp.tests.common.models.TestData import TestData
from HolidayBookingApp.domains.request.models.Request import Request
from datetime import datetime
from HolidayBookingApp.common.enums.RequestStatus import RequestStatus


def test_create_request_id_set_to_1_when_no_other_requests_exist_data():
    method_parameters = ["2020-12-1",
                         "2020-12-10",
                         1,
                         2,
                         10]
    method_query_order = ["SELECT request_id FROM requests ORDER BY request_id DESC LIMIT 1",
                          "INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)"]
    expected_values = [[]]
    expected_parameters = [None,
                           ['1', "2020-12-1", "2020-12-10", "1", "2", "pending", "10"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_create_request_id_incremented_by_1_when_other_requests_exist_data():
    method_parameters = ["2020-12-1",
                         "2020-12-10",
                         1,
                         2,
                         10]
    method_query_order = ["SELECT request_id FROM requests ORDER BY request_id DESC LIMIT 1",
                          "INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)"]
    expected_values = [[[(1)]]]
    expected_parameters = [None,
                           ['2', "2020-12-1", "2020-12-10", "1", "2", "pending", "10"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_get_requests_for_approval_returns_correct_results_when_requests_exist_data():
    method_parameters = [2]
    method_query_order = ["SELECT requests.request_id, users.first_name, users.surname, "
                          "requests.start_date, requests.end_date, requests.total_holidays "
                          "FROM requests "
                          "JOIN users ON requests.employee_id = users.user_id "
                          "WHERE requests.approver_id = ? AND "
                          "requests.request_status = 'pending'"]

    expected_values = [[(1, "Test", "Test", "2020-12-1", "2020-12-10", 10),
                        (2, "Test", "Test", "2021-12-1", "2021-12-10", 10)]]
    expected_parameters = [["2"]]

    expected_result = [Request(1,
                               "Test",
                               "Test",
                               datetime(2020, 12, 1),
                               datetime(2020, 12, 10),
                               10,
                               "pending"),
                       Request(2,
                               "Test",
                               "Test",
                               datetime(2021, 12, 1),
                               datetime(2021, 12, 10),
                               10,
                               "pending")
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_requests_for_review_returns_correct_results_when_requests_exist_data():
    method_parameters = [2]
    method_query_order = ["SELECT request_id, users.first_name, users.surname, "
                          "start_date, end_date, requests.total_holidays, "
                          "requests.request_status "
                          "FROM requests "
                          "LEFT JOIN users ON requests.approver_id = users.user_id "
                          "WHERE requests.employee_id = ? "
                          "ORDER BY request_id DESC"]

    expected_values = [[(1, "Test", "Test", "2020-12-1", "2020-12-10", 10),
                        (2, "Test", "Test", "2021-12-1", "2021-12-10", 10)]]
    expected_parameters = [["2"]]

    expected_result = [Request(1,
                               "Test",
                               "Test",
                               datetime(2020, 12, 1),
                               datetime(2020, 12, 10),
                               10,
                               "pending"),
                       Request(2,
                               "Test",
                               "Test",
                               datetime(2021, 12, 1),
                               datetime(2021, 12, 10),
                               10,
                               "pending")
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_approve_request_request_approved_when_method_called_data():
    method_parameters = [1]
    method_query_order = ["SELECT total_holidays, employee_id FROM requests WHERE request_id = ?",
                          "UPDATE requests SET request_status = 'approved' WHERE request_id = ?",
                          "UPDATE users SET holidays_remaining = holidays_remaining - ? WHERE user_id = ?"]

    expected_values = [[(10, 1)]]
    expected_parameters = [["1"],
                           ["1"],
                           ["10", "1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_reject_request_request_rejected_when_method_called_data():
    method_parameters = [1]
    method_query_order = ["UPDATE requests SET request_status = 'rejected' WHERE request_id = ?"]

    expected_values = [[]]
    expected_parameters = [["1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_cancel_request_request_cancelled_when_method_called_data():
    method_parameters = [1]
    method_query_order = ["UPDATE requests SET request_status = 'cancelled' WHERE request_id = ?"]

    expected_values = [[]]
    expected_parameters = [["1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_get_pending_holidays_holidays_total_returned_when_pending_holidays_exist_data():
    method_parameters = [1]
    method_query_order = ["SELECT SUM(total_holidays) FROM requests WHERE "
                          "employee_id = ? AND request_status = 'pending'"]

    expected_values = [[(10,)]]
    expected_parameters = [["1"]]
    expected_result = 10

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_pending_holidays_holidays_0_returned_when_pending_holidays_do_not_exist_data():
    method_parameters = [1]
    method_query_order = ["SELECT SUM(total_holidays) FROM requests WHERE "
                          "employee_id = ? AND request_status = 'pending'"]

    expected_values = [[(None,)]]
    expected_parameters = [["1"]]
    expected_result = 0

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_live_request_history_request_history_returned_when_requests_exist_data():
    method_parameters = [1]
    method_query_order = ["SELECT * FROM requests WHERE employee_id = ? AND request_status IN ('approved', 'pending')"]

    expected_values = [[(1, '2020-12-1', '2020-12-31', "", "", "pending"),
                        (2, '2021-12-1', '2021-12-31', "", "", "approved")]]
    expected_parameters = [["1"]]
    expected_result = [Request(1,
                               "",
                               "",
                               datetime(2020, 12, 1),
                               datetime(2020, 12, 31),
                               0,
                               "pending"),
                       Request(2,
                               "",
                               "",
                               datetime(2021, 12, 1),
                               datetime(2021, 12, 31),
                               0,
                               "approved")
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_all_requests_by_status_requests_returned_when_requests_exist_data():
    method_parameters = [RequestStatus.pending]
    method_query_order = ["SELECT request_id, start_date, end_date FROM requests WHERE request_status = ?"]

    expected_values = [[(1, '2020-12-1', '2020-12-31', "", "", "pending"),
                        (2, '2021-12-1', '2021-12-31', "", "", "pending")]]
    expected_parameters = [["pending"]]
    expected_result = [Request(1,
                               "",
                               "",
                               '2020-12-1',
                               '2020-12-31',
                               0,
                               "pending"),
                       Request(2,
                               "",
                               "",
                               '2021-12-1',
                               '2021-12-31',
                               0,
                               "pending")
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)