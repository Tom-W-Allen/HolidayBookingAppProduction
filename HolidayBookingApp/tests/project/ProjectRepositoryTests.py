from unittest import TestCase
from HolidayBookingApp.domains.project.ProjectRepository import ProjectRepository
from HolidayBookingApp.tests.common.TestExecution import *
from HolidayBookingApp.tests.project.ProjectTestData import *
from datetime import datetime, date

_connection_string = "persistence/HolidayBookingDatabase.db"
_class_under_test = "domains.project.ProjectRepository"
_sut = ProjectRepository(_connection_string)
_test_executor = TestExecutor(_sut, _class_under_test)
_current_date = datetime(date.today().year, date.today().month, date.today().day)


class ProjectRepositoryMethodTests(TestCase):

    # region validate_project_dates tests
    def test_validate_project_dates_None_returned_when_valid_dates_provided(self):
        expected_result = None

        test_data = test_validate_project_dates_None_returned_when_valid_dates_provided_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_start_date_less_than_end_date(self):
        expected_result = "End date must be after start date."

        test_data = test_validate_project_dates_error_returned_when_start_date_less_than_end_date_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_start_date_less_than_current_date(self):
        expected_result = "All dates in selected range must be after the current date."

        test_data = test_validate_project_dates_error_returned_when_start_date_less_than_current_date()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_start_date_is_current_date(self):
        expected_result = "All dates in selected range must be after the current date."

        test_data = test_validate_project_dates_error_returned_when_start_date_is_current_date_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_project_booked_for_weekend(self):
        expected_result = "No weekdays selected, projects must be completed in work hours."

        test_data = test_validate_project_dates_error_returned_when_project_booked_for_weekend_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_start_date_is_blank(self):
        expected_result = "Please select a date from both fields."

        test_data = test_validate_project_dates_error_returned_when_start_date_is_blank_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_end_date_is_blank(self):
        expected_result = "Please select a date from both fields."

        test_data = test_validate_project_dates_error_returned_when_end_date_is_blank_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    def test_validate_project_dates_error_returned_when_project_name_exists(self):
        expected_result = "Project name is already in use"

        test_data = test_validate_project_dates_error_returned_when_project_name_exists_data()

        actual_result = _test_executor.execute_test(test_data, 'validate_project_dates')

        self.assertEqual(expected_result, actual_result.message)

    # endregion

    # region create_project tests
    def test_create_project_project_id_set_as_1_if_no_other_projects_exist(self):

        test_data = test_create_project_project_id_set_as_1_if_no_other_projects_exist_data()

        actual_result = _test_executor.execute_test(test_data, 'create_project')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_create_project_project_id_incremented_by_1_when_other_projects_exist(self):

        test_data = test_create_project_project_id_incremented_by_1_when_other_projects_exist_data()

        actual_result = _test_executor.execute_test(test_data, 'create_project')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_create_project_project_id_incremented_by_1_when_only_one_table_has_records(self):

        test_data = test_create_project_project_id_incremented_by_1_when_only_one_table_has_records_data()

        actual_result = _test_executor.execute_test(test_data, 'create_project')

        self.assertEqual(test_data.expected_result, actual_result)
    # endregion

    def test_get_all_projects_date_converted_to_datetime_when_projects_returned(self):

        test_data = test_get_all_projects_date_converted_to_datetime_when_projects_returned_data()

        actual_result = _test_executor.execute_test(test_data, 'get_all_projects')

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].project_id, actual_result[i].project_id)
            self.assertEqual(test_data.expected_result[i].project_name, actual_result[i].project_name)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].project_lead, actual_result[i].project_lead)

    def test_get_all_projects_empty_list_returned_when_no_projects_available(self):

        test_data = test_get_all_projects_empty_list_returned_when_no_projects_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_all_projects')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_manager_projects_date_converted_to_datetime_when_projects_returned(self):

        test_data = get_manager_projects_date_converted_to_datetime_when_projects_returned_data()

        actual_result = _test_executor.execute_test(test_data, 'get_manager_projects')

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].project_id, actual_result[i].project_id)
            self.assertEqual(test_data.expected_result[i].project_name, actual_result[i].project_name)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].project_lead, actual_result[i].project_lead)

    def test_get_manager_projects_empty_list_returned_when_no_projects_available(self):

        test_data = test_get_manager_projects_empty_list_returned_when_no_projects_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_manager_projects')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_employee_projects_date_converted_to_datetime_when_projects_returned(self):
        test_data = test_get_employee_projects_date_converted_to_datetime_when_projects_returned_data()

        actual_result = _test_executor.execute_test(test_data, 'get_employee_projects')

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].project_id, actual_result[i].project_id)
            self.assertEqual(test_data.expected_result[i].project_name, actual_result[i].project_name)
            self.assertEqual(test_data.expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(test_data.expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(test_data.expected_result[i].project_lead, actual_result[i].project_lead)

    def test_get_employee_projects_empty_list_returned_when_no_projects_available(self):

        test_data = test_get_employee_projects_empty_list_returned_when_no_projects_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_employee_projects')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_available_employees_correct_results_returned_when_employees_available(self):

        test_data = test_get_available_employees_correct_results_returned_when_employees_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_available_employees')

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(test_data.expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(test_data.expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].manager, actual_result[i].manager)

    def test_get_available_employees_empty_list_returned_when_no_employees_available(self):

        test_data = test_get_available_employees_empty_list_returned_when_no_employees_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_available_employees')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_enrolled_employees_correct_results_returned_when_employees_available(self):

        test_data = test_get_enrolled_employees_correct_results_returned_when_employees_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_enrolled_employees')

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(test_data.expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(test_data.expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].project_holidays, actual_result[i].project_holidays)

    def test_get_enrolled_employees_empty_list_returned_when_no_employees_available(self):

        test_data = test_get_enrolled_employees_empty_list_returned_when_no_employees_available_data()

        actual_result = _test_executor.execute_test(test_data, 'get_enrolled_employees')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_add_employee_to_project_record_inserted_when_no_preexisting_record(self):

        test_data = test_add_employee_to_project_record_inserted_when_no_preexisting_record_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, 'add_employee_to_project')

    def test_add_employee_to_project_record_updated_when_preexisting_record_exists(self):

        test_data = test_add_employee_to_project_record_updated_when_preexisting_record_exists()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, 'add_employee_to_project')

    def test_remove_employee_from_project_sql_executes_correctly_when_method_is_called(self):

        test_data = test_remove_employee_from_project_sql_executes_correctly_when_method_is_called_data()

        # Void method, hence cannot check return values
        _test_executor.execute_test(test_data, 'remove_employee_from_project')

    def test_find_project_name_returns_true_when_project_exists(self):

        test_data = test_find_project_name_sql_executes_correctly_when_method_is_called_data()

        # Void method, hence cannot check return values
        actual_result = _test_executor.execute_test(test_data, 'find_project_name')

        self.assertTrue(actual_result)

    def test_find_project_name_returns_false_when_project_does_not_exist(self):

        test_data = test_find_project_name_returns_false_when_project_does_not_exist_data()

        # Void method, hence cannot check return values
        actual_result = _test_executor.execute_test(test_data, 'find_project_name')

        self.assertFalse(actual_result)

    def test_get_project_overlap_holidays_returns_empty_list_when_no_overlap(self):

        test_data = test_get_project_overlap_holidays_returns_empty_list_when_no_overlap_data()

        actual_result = _test_executor.execute_test(test_data, 'get_project_overlap_holidays')

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_project_overlap_holidays_returns_correct_results_when_overlap_exists(self):

        test_data = test_get_project_overlap_holidays_returns_correct_results_when_overlap_exists_data()

        actual_result = _test_executor.execute_test(test_data, 'get_project_overlap_holidays')

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(test_data.expected_result)):
            self.assertEqual(test_data.expected_result[i], actual_result[i])
