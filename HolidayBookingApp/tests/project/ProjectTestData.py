from HolidayBookingApp.tests.common.models.TestData import TestData
from datetime import datetime, date, timedelta
from HolidayBookingApp.domains.project.models.Project import Project
from HolidayBookingApp.domains.project.models.ProjectMember import ProjectMember
from HolidayBookingApp.domains.user.models.PublicUser import PublicUser

_current_date = datetime(date.today().year, date.today().month, date.today().day)


def test_create_project_project_id_set_as_1_if_no_other_projects_exist_data():
    method_parameters = ["Test project name",
                         datetime(2020, 12, 1),
                         datetime(2020, 12, 30),
                         '1']
    method_query_order = ["SELECT project_id FROM projects ORDER BY project_id DESC LIMIT 1",
                          "SELECT project_id FROM employee_projects ORDER BY project_id DESC LIMIT 1",
                          "INSERT INTO projects VALUES (?, ?, ?, ?, ?)"]
    expected_values = [[],
                       []]
    expected_parameters = [None,
                           None,
                           ['1', "Test project name", '2020-12-01 00:00:00', '2020-12-30 00:00:00', '1']]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_create_project_project_id_incremented_by_1_when_other_projects_exist_data():
    method_parameters = ["Test project name",
                         datetime(2020, 12, 1),
                         datetime(2020, 12, 30),
                         '1']
    method_query_order = ["SELECT project_id FROM projects ORDER BY project_id DESC LIMIT 1",
                          "SELECT project_id FROM employee_projects ORDER BY project_id DESC LIMIT 1",
                          "INSERT INTO projects VALUES (?, ?, ?, ?, ?)"]
    expected_values = [[(111,)],
                       [(110,)]]
    expected_parameters = [None,
                           None,
                           ['112', "Test project name", '2020-12-01 00:00:00', '2020-12-30 00:00:00', '1']]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_create_project_project_id_incremented_by_1_when_only_one_table_has_records_data():
    method_parameters = ["Test project name",
                         datetime(2020, 12, 1),
                         datetime(2020, 12, 30),
                         '1']
    method_query_order = ["SELECT project_id FROM projects ORDER BY project_id DESC LIMIT 1",
                          "SELECT project_id FROM employee_projects ORDER BY project_id DESC LIMIT 1",
                          "INSERT INTO projects VALUES (?, ?, ?, ?, ?)"]
    expected_values = [[(111,)],
                       []]
    expected_parameters = [None,
                           None,
                           ['112', "Test project name", '2020-12-01 00:00:00', '2020-12-30 00:00:00', '1']]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_None_returned_when_valid_dates_provided_data():
    test_project = "Test"
    test_start_date = _current_date + timedelta(10)
    test_end_date = _current_date + timedelta(40)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_start_date_is_current_date_data():
    test_project = "Test"
    test_end_date = _current_date + timedelta(5)

    test_start_date = datetime.strftime(_current_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_start_date_less_than_current_date():
    test_project = "Test"
    test_start_date = _current_date - timedelta(1)
    test_end_date = _current_date + timedelta(5)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_start_date_less_than_end_date_data():
    test_project = "Test"
    test_start_date = _current_date + timedelta(10)
    test_end_date = _current_date + timedelta(5)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_project_booked_for_weekend_data():
    test_project = "Test"
    current_weekday = _current_date.isoweekday()
    # Find days from today to next Saturday
    advance = 7 - (current_weekday - 6) if current_weekday > 5 else 6 - current_weekday
    test_start_date = _current_date + timedelta(advance)
    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = _current_date + timedelta(advance + 1)
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_start_date_is_blank_data():
    test_project = "Test"
    test_start_date = ""
    test_end_date = datetime.strftime(_current_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_end_date_is_blank_data():
    test_project = "Test"
    test_start_date = datetime.strftime(_current_date, "%Y-%m-%d")
    test_end_date = ""

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_validate_project_dates_error_returned_when_project_name_exists_data():
    test_project = "Test"
    test_start_date = _current_date + timedelta(10)
    test_end_date = _current_date + timedelta(40)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    method_parameters = [test_start_date, test_end_date, test_project]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]
    expected_values = [["Test"]]
    expected_parameters = [[test_project]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_get_all_projects_date_converted_to_datetime_when_projects_returned_data():

    method_parameters = []
    expected_values = [[(1, "Test", "2020-5-30", "2021-5-30", 1),
                        (2, "Test 2", "2023-12-1", "2024-12-1", 2)]]
    expected_parameters = [None]
    method_query_order = ["SELECT project_id, project_name, start_date, end_date, project_lead_id FROM projects"]
    expected_result = [Project(1,
                               "Test",
                               datetime(2020, 5, 30),
                               datetime(2021, 5, 30),
                               1),
                       Project(2,
                               "Test 2",
                               datetime(2023, 12, 1),
                               datetime(2024, 12, 1),
                               2)
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_all_projects_empty_list_returned_when_no_projects_available_data():
    method_parameters = []
    expected_values = [[]]
    expected_parameters = [None]
    method_query_order = ["SELECT project_id, project_name, start_date, end_date, project_lead_id FROM projects"]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def get_manager_projects_date_converted_to_datetime_when_projects_returned_data():
    method_parameters = [1]
    expected_values = [[(1, "Test", "2020-5-30", "2021-5-30", 1),
                        (2, "Test 2", "2023-12-1", "2024-12-1", 1)]]
    expected_parameters = [['1']]
    method_query_order = ["SELECT project_id, project_name, start_date, end_date "
                          "FROM projects WHERE project_lead_id = ?"]
    expected_result = [Project(1,
                               "Test",
                               datetime(2020, 5, 30),
                               datetime(2021, 5, 30),
                               1),
                       Project(2,
                               "Test 2",
                               datetime(2023, 12, 1),
                               datetime(2024, 12, 1),
                               1)
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_manager_projects_empty_list_returned_when_no_projects_available_data():

    method_parameters = [1]
    expected_values = [[]]
    expected_parameters = [['1']]
    method_query_order = ["SELECT project_id, project_name, start_date, end_date "
                          "FROM projects WHERE project_lead_id = ?"]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_employee_projects_date_converted_to_datetime_when_projects_returned_data():

    string_today = _current_date.strftime("%Y-%m-%d")
    method_parameters = [1]
    expected_values = [[(1, "Test", "2020-5-30", "2021-5-30", 1),
                        (2, "Test 2", "2023-12-1", "2024-12-1", 1)]]
    expected_parameters = [['1', string_today]]
    method_query_order = ["SELECT projects.project_id, projects.project_name, "
                          "projects.start_date, projects.end_date, projects.project_lead_id "
                          "FROM projects "
                          "JOIN employee_projects ON "
                          "projects.project_id = employee_projects.project_id "
                          "WHERE employee_projects.employee_id = ? AND "
                          "employee_projects.leave_date > ?"]
    expected_result = [Project(1,
                               "Test",
                               datetime(2020, 5, 30),
                               datetime(2021, 5, 30),
                               1),
                       Project(2,
                               "Test 2",
                               datetime(2023, 12, 1),
                               datetime(2024, 12, 1),
                               1)
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_employee_projects_empty_list_returned_when_no_projects_available_data():

    string_today = _current_date.strftime("%Y-%m-%d")
    method_parameters = [1]
    expected_values = [[]]
    expected_parameters = [['1', string_today]]
    method_query_order = ["SELECT projects.project_id, projects.project_name, "
                          "projects.start_date, projects.end_date, projects.project_lead_id "
                          "FROM projects "
                          "JOIN employee_projects ON "
                          "projects.project_id = employee_projects.project_id "
                          "WHERE employee_projects.employee_id = ? AND "
                          "employee_projects.leave_date > ?"]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_available_employees_correct_results_returned_when_employees_available_data():
    string_today = _current_date.strftime("%Y-%m-%d")
    method_parameters = [1, 1]
    expected_values = [[(1, "Test User Name", 'basic', "Test First Name", "Test Surname", 5),
                        (2, "Test User Name2", 'basic', "Test First Name2", "Test Surname2", 5)]]
    expected_parameters = [['1', '1', string_today]]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname, manager "
                          "FROM users AS u1 "
                          "WHERE "
                          "manager = ? AND "
                          "NOT EXISTS (SELECT * FROM employee_projects WHERE "
                          "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)"]
    expected_result = [PublicUser(1,
                                  "Test User Name",
                                  'basic',
                                  "Test First Name",
                                  "Test Surname",
                                  5),
                       PublicUser(2,
                                  "Test User Name2",
                                  'basic',
                                  "Test First Name2",
                                  "Test Surname2",
                                  5)
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_available_employees_empty_list_returned_when_no_employees_available_data():
    string_today = _current_date.strftime("%Y-%m-%d")
    method_parameters = [1, 1]
    expected_values = [[]]
    expected_parameters = [['1', '1', string_today]]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname, manager "
                          "FROM users AS u1 "
                          "WHERE "
                          "manager = ? AND "
                          "NOT EXISTS (SELECT * FROM employee_projects WHERE "
                          "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)"]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_enrolled_employees_correct_results_returned_when_employees_available_data():
    string_today = _current_date.strftime("%Y-%m-%d")
    method_parameters = [1, 1]
    expected_values = [[(1, "Test User Name", 'basic', "Test First Name", "Test Surname", 5)],
                       [("2020-5-30", "2020-6-3")],
                       []]
    expected_parameters = [['1', '1', string_today],
                           ['1'],
                           ['1']]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname "
                          "FROM users AS u1 "
                          "WHERE "
                          "manager = ? AND "
                          "EXISTS (SELECT * FROM employee_projects WHERE "
                          "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)",

                          "SELECT start_date, end_date FROM projects WHERE "
                          "project_id = ? LIMIT 1",

                          "SELECT start_date, end_date "
                          "FROM requests "
                          "WHERE employee_id = ? AND request_status = 'approved'"
                          ]
    expected_result = [ProjectMember(1,
                                     "Test User Name",
                                     'basic',
                                     "Test First Name",
                                     "Test Surname",
                                     [])
                       ]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_enrolled_employees_empty_list_returned_when_no_employees_available_data():
    string_today = _current_date.strftime("%Y-%m-%d")
    method_parameters = [1, 1]
    expected_values = [[],
                       [("2020-5-30", "2020-6-3")],
                       []]
    expected_parameters = [['1', '1', string_today],
                           ['1'],
                           ['1']]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname "
                          "FROM users AS u1 "
                          "WHERE "
                          "manager = ? AND "
                          "EXISTS (SELECT * FROM employee_projects WHERE "
                          "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)",

                          "SELECT start_date, end_date FROM projects WHERE "
                          "project_id = ? LIMIT 1",

                          "SELECT start_date, end_date "
                          "FROM requests "
                          "WHERE employee_id = ? AND request_status = 'approved'"
                          ]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_add_employee_to_project_record_inserted_when_no_preexisting_record_data():
    method_parameters = [1, 1]
    expected_values = [[("2020-5-30", "2020-6-3")],
                       []]
    expected_parameters = [['1'],
                           ['1', '1'],
                           ['1', '1', "2020-5-30", "2020-6-3"]]
    method_query_order = ["SELECT start_date, end_date FROM projects WHERE project_id = ?",
                          "SELECT * FROM employee_projects WHERE employee_id = ? AND project_id = ?",
                          "INSERT INTO employee_projects VALUES (?, ?, ? ,?)"
                          ]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_add_employee_to_project_record_updated_when_preexisting_record_exists():
    string_today = _current_date.strftime("%Y-%m-%d")

    method_parameters = [1, 1]
    expected_values = [[("2020-5-30", "2020-6-3")],
                       ["Test record"]]
    expected_parameters = [['1'],
                           ['1', '1'],
                           [string_today, "2020-6-3", '1', '1']]
    method_query_order = ["SELECT start_date, end_date FROM projects WHERE project_id = ?",

                          "SELECT * FROM employee_projects WHERE employee_id = ? AND project_id = ?",

                          "UPDATE employee_projects SET join_date = ?, leave_date = ? "
                          "WHERE employee_id = ? AND project_id = ?"
                          ]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_remove_employee_from_project_sql_executes_correctly_when_method_is_called_data():
    string_today = _current_date.strftime("%Y-%m-%d")

    method_parameters = [1, 1]
    expected_values = []
    expected_parameters = [[string_today, "1", "1"]]
    method_query_order = ["UPDATE employee_projects SET leave_date = ? WHERE employee_id = ? AND project_id = ?"]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_find_project_name_sql_executes_correctly_when_method_is_called_data():
    method_parameters = ["Test name"]
    expected_values = [["Test name"]]
    expected_parameters = [["Test name"]]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_find_project_name_returns_false_when_project_does_not_exist_data():
    method_parameters = ["Test name"]
    expected_values = [[]]
    expected_parameters = [["Test name"]]
    method_query_order = ["SELECT * FROM projects WHERE project_name = ? LIMIT 1"]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_get_project_overlap_holidays_returns_empty_list_when_no_overlap_data():
    method_parameters = [1, 1]
    expected_values = [[("2024-2-26", "2024-8-2")],
                       [("2024-1-1", "2024-1-2", "2024-1-3", "2024-1-4", "2024-1-5")]]
    expected_parameters = [['1'],
                           ['1']]
    method_query_order = ["SELECT start_date, end_date FROM projects WHERE project_id = ? LIMIT 1",

                          "SELECT start_date, end_date FROM requests "
                          "WHERE employee_id = ? AND request_status = 'approved'"
                          ]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_project_overlap_holidays_returns_correct_results_when_overlap_exists_data():
    method_parameters = [1, 1]
    expected_values = [[("2024-1-1", "2024-1-3")],
                       [("2024-1-1", "2024-1-5")]]
    expected_parameters = [['1'],
                           ['1']]
    method_query_order = ["SELECT start_date, end_date FROM projects WHERE project_id = ? LIMIT 1",

                          "SELECT start_date, end_date FROM requests "
                          "WHERE employee_id = ? AND request_status = 'approved'"
                          ]
    expected_result = [datetime(2024, 1, 1),
                       datetime(2024, 1, 2),
                       datetime(2024, 1, 3)]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)
