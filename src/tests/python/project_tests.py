from unittest import TestCase
from unittest.mock import MagicMock, patch

from domains.project.ProjectRepository import ProjectRepository
from domains.project.models.ProjectValidationDetails import ProjectValidationDetails
from domains.project.models.Project import Project
from domains.project.models.ProjectMember import ProjectMember
from domains.user.models.PublicUser import PublicUser
from common.enums.State import State
from data.ProjectTestData import *
from datetime import datetime, date
from persistence.Database import Database

_database = MagicMock()
_sut = ProjectRepository(_database)
_current_date = datetime(date.today().year, date.today().month, date.today().day)


class ProjectRepositoryMethodTests(TestCase):

    @patch.object(ProjectRepository, "find_project_name", find_project_name)
    def test_validate_project_dates_None_returned_when_valid_dates_provided(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_1_method_parameters()

        expected_result = ProjectValidationDetails(State.Success, None)
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(ProjectRepository, "find_project_name", find_project_name)
    def test_validate_project_dates_error_returned_when_start_date_less_than_current_date(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_2_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning,
                                                   "All dates in selected range must "
                                                   "be after the current date.")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(ProjectRepository, "find_project_name", find_project_name)
    def test_validate_project_dates_error_returned_when_project_booked_for_weekend(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_3_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning,
                                                   "No weekdays selected, projects must "
                                                   "be completed in work hours.")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(ProjectRepository, "find_project_name", find_project_name)
    def test_validate_project_dates_error_returned_when_start_date_less_than_end_date(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_4_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning,
                                                   "End date must be after start date.")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(ProjectRepository, "find_project_name", find_project_name)
    def test_validate_project_dates_error_returned_when_start_date_is_blank(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_5_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning,
                                                   "Please select a date from both fields.")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(ProjectRepository, "find_project_name", find_project_name)
    def test_validate_project_dates_error_returned_when_end_date_is_blank(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_6_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning,
                                                   "Please select a date from both fields.")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(ProjectRepository, "find_project_name", find_project_name_exists)
    def test_validate_project_dates_error_returned_when_project_name_exists(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_7_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning,
                                                   "Project name is already in use")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(Database, "query_database", test_8_query_function)
    def test_create_project_project_id_set_as_1_if_no_other_projects_exist(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_8_method_parameters()

        sut.create_project(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_9_query_function)
    def test_create_project_project_id_incremented_by_1_when_other_projects_exist(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_9_method_parameters()

        sut.create_project(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_10_query_function)
    def test_create_project_project_id_incremented_by_1_when_only_one_table_has_records(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_10_method_parameters()

        sut.create_project(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_11_query_function)
    def test_get_all_projects_date_converted_to_datetime_when_projects_returned(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)

        start_date = datetime(2020, 5, 30)
        end_date = datetime(2021, 5, 30)

        expected_result = [Project("1", "Test Name", start_date, end_date, "2"),
                           Project("2", "Test Name 2", start_date, end_date, "3")]
        actual_result = sut.get_all_projects()

        self.assertGreater(len(actual_result), 0)

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].project_id, actual_result[i].project_id)
            self.assertEqual(expected_result[i].project_name, actual_result[i].project_name)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].project_lead, actual_result[i].project_lead)

    def test_validate_project_dates_error_returned_when_start_date_is_current_date(self):
        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_12_method_parameters()

        expected_result = ProjectValidationDetails(State.Warning, "All dates in selected range must be "
                                                                  "after the current date.")
        actual_result = sut.validate_project_dates(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.state, actual_result.state)
        self.assertEqual(expected_result.message, actual_result.message)

    @patch.object(Database, "query_database", test_13_query_function)
    def test_get_all_projects_empty_list_returned_when_no_projects_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)

        expected_result = []
        actual_result = sut.get_all_projects()

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_14_query_function)
    def test_get_manager_projects_date_converted_to_datetime_when_projects_returned(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_14_method_parameters()

        start_date = datetime(2020, 5, 30)
        end_date = datetime(2021, 5, 30)

        expected_result = [Project("1", "Test Name", start_date, end_date, 2),
                           Project("2", "Test Name 2", start_date, end_date, 2)]

        actual_result = sut.get_manager_projects(*[arg for arg in input_parameters])

        self.assertGreater(len(actual_result), 0)

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].project_id, actual_result[i].project_id)
            self.assertEqual(expected_result[i].project_name, actual_result[i].project_name)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].project_lead, actual_result[i].project_lead)

    @patch.object(Database, "query_database", test_15_query_function)
    def test_get_manager_projects_empty_list_returned_when_no_projects_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_15_method_parameters()
        expected_result = []

        actual_result = sut.get_manager_projects(*[arg for arg in input_parameters])

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_16_query_function)
    def test_get_employee_projects_date_converted_to_datetime_when_projects_returned(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_16_method_parameters()

        start_date = datetime(2020, 5, 30)
        end_date = datetime(2021, 5, 30)

        expected_result = [Project("1", "Test Name", start_date, end_date, "2"),
                           Project("2", "Test Name 2", start_date, end_date, "2")]

        actual_result = sut.get_employee_projects(*[arg for arg in input_parameters])

        self.assertGreater(len(actual_result), 0)

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].project_id, actual_result[i].project_id)
            self.assertEqual(expected_result[i].project_name, actual_result[i].project_name)
            self.assertEqual(expected_result[i].start_date, actual_result[i].start_date)
            self.assertEqual(expected_result[i].end_date, actual_result[i].end_date)
            self.assertEqual(expected_result[i].project_lead, actual_result[i].project_lead)

    @patch.object(Database, "query_database", test_17_query_function)
    def test_get_employee_projects_empty_list_returned_when_no_projects_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_17_method_parameters()

        expected_result = []

        actual_result = sut.get_employee_projects(*[arg for arg in input_parameters])

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_18_query_function)
    def test_get_available_employees_correct_results_returned_when_employees_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_18_method_parameters()

        expected_result = [PublicUser("1", "Test Username", "basic", "Test Name",
                                     "Test Surname", "2", "Test Email"),
                           PublicUser("3", "Test Username", "basic", "Test Name",
                                      "Test Surname", "2", "Test Email")]

        actual_result = sut.get_available_employees(*[arg for arg in input_parameters])

        self.assertGreater(len(actual_result), 0)

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].manager, actual_result[i].manager)

    @patch.object(Database, "query_database", test_19_query_function)
    def test_get_available_employees_empty_list_returned_when_no_employees_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_19_method_parameters()

        expected_result = []

        actual_result = sut.get_available_employees(*[arg for arg in input_parameters])

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_20_query_function)
    @patch.object(ProjectRepository, "get_project_overlap_holidays", test_20_get_project_overlap_holidays)
    def test_get_enrolled_employees_correct_results_returned_when_employees_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_20_method_parameters()

        member_1_holidays = [datetime(2020, 5, 10), datetime(2020, 6, 8)]
        member_2_holidays = [datetime(2020, 5, 7)]

        expected_result = [ProjectMember(1, "Test Username", "basic", "Test Name",
                                     "Test Surname",  member_1_holidays),
                           ProjectMember(3, "Test Username", "basic", "Test Name",
                                      "Test Surname", member_2_holidays)]

        actual_result = sut.get_enrolled_employees(*[arg for arg in input_parameters])

        self.assertGreater(len(actual_result), 0)

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].project_holidays, actual_result[i].project_holidays)

    @patch.object(Database, "query_database", test_21_query_function)
    @patch.object(ProjectRepository, "get_project_overlap_holidays", test_21_get_project_overlap_holidays)
    def test_get_enrolled_employees_empty_list_returned_when_no_employees_available(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_21_method_parameters()

        expected_result = []

        actual_result = sut.get_enrolled_employees(*[arg for arg in input_parameters])

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_22_query_function)
    def test_add_employee_to_project_record_inserted_when_no_preexisting_record(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_22_method_parameters()

        sut.add_employee_to_project(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_23_query_function)
    def test_add_employee_to_project_record_updated_when_preexisting_record_exists(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_23_method_parameters()

        sut.add_employee_to_project(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_24_query_function)
    def test_remove_employee_from_project_sql_executes_correctly_when_method_is_called(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_24_method_parameters()

        sut.remove_employee_from_project(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_25_query_function)
    def test_find_project_name_returns_true_when_project_exists(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_25_method_parameters()

        actual_result = sut.find_project_name(*[arg for arg in input_parameters])

        self.assertTrue(actual_result)

    @patch.object(Database, "query_database", test_26_query_function)
    def test_find_project_name_returns_false_when_project_does_not_exist(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_26_method_parameters()

        actual_result = sut.find_project_name(*[arg for arg in input_parameters])

        self.assertFalse(actual_result)

    @patch.object(Database, "query_database", test_27_query_function)
    def test_get_project_overlap_holidays_returns_correct_results_when_overlap_exists(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_27_method_parameters()

        expected_result = [datetime(2020, 5, 10), datetime(2020, 5, 11)]
        actual_result = sut.get_project_overlap_holidays(*[arg for arg in input_parameters])

        self.assertEqual(expected_result, actual_result)

    @patch.object(Database, "query_database", test_28_query_function)
    def test_get_project_overlap_holidays_returns_empty_list_when_no_overlap(self):

        mock_database = Database()
        sut = ProjectRepository(mock_database)
        input_parameters = test_28_method_parameters()

        expected_result = []
        actual_result = sut.get_project_overlap_holidays(*[arg for arg in input_parameters])

        self.assertEqual(expected_result, actual_result)
