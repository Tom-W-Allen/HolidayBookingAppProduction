from unittest import TestCase, main
from HolidayBookingApp.domains.user.UserRepository import UserRepository
from HolidayBookingApp.tests.common.TestExecution import *
from HolidayBookingApp.tests.user.UserTestData import *

_connection_string = "persistence/HolidayBookingDatabase.db"
_class_under_test = "domains.user.UserRepository"
_sut = UserRepository(_connection_string)
_test_executor = TestExecutor(_sut, _class_under_test)


class UserRepositoryMethodTests(TestCase):

    def test_add_user_sets_id_as_1_when_no_users_in_database(self):

        test_data = test_add_user_sets_id_as_1_when_no_users_in_database_data()

        actual_result = _test_executor.execute_test(test_data, "add_user")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_add_user_increments_id_when_users_already_exist(self):

        test_data = test_add_user_increments_id_when_users_already_exist_data()

        actual_result = _test_executor.execute_test(test_data, "add_user")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_add_user_manager_id_set_when_not_none(self):

        test_data = test_add_user_manager_id_set_when_not_none_data()

        actual_result = _test_executor.execute_test(test_data, "add_user")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_user_manager_id_returned_when_manager_exists(self):

        test_data = test_get_user_manager_id_returned_when_manager_exists_data()

        actual_result = _test_executor.execute_test(test_data, "get_user_manager")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_user_manager_negative_1_returned_when_manager_does_not_exist(self):

        test_data = test_get_user_negative_1_returned_when_manager_does_not_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_user_manager")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_user_type_details_empty_list_returned_when_no_users_exist(self):

        test_data = test_get_user_type_details_empty_list_returned_when_no_users_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_user_type_details")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_user_type_details_list_returned_when_users_exist(self):

        test_data = test_get_user_type_details_list_returned_when_users_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_user_type_details")

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(test_data.expected_result)):
            self.assertEqual(test_data.expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(test_data.expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(test_data.expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)

    def test_get_user_login_details_none_returned_when_no_user_exists(self):

        test_data = test_get_user_login_details_none_returned_when_no_user_exists_data()

        actual_result = _test_executor.execute_test(test_data, "get_user_login_details")

        self.assertEqual(test_data.expected_result, actual_result)

    def test_get_user_login_details_details_returned_when_user_exists(self):

        test_data = test_get_user_login_details_details_returned_when_user_exists_data()

        actual_result = _test_executor.execute_test(test_data, "get_user_login_details")

        self.assertEqual(test_data.expected_result.user_id, actual_result.user_id)
        self.assertEqual(test_data.expected_result.user_name, actual_result.user_name)
        self.assertEqual(test_data.expected_result.password, actual_result.password)
        self.assertEqual(test_data.expected_result.user_role, actual_result.user_role)

    def test_check_username_exists_returns_True_if_user_exists(self):

        test_data = test_check_username_exists_returns_True_if_user_exists_data()

        actual_result = _test_executor.execute_test(test_data, "check_username_exists")

        self.assertTrue(actual_result)

    def test_check_username_exists_returns_False_if_user_does_not_exist(self):

        test_data = test_check_username_exists_returns_False_if_user_does_not_exist_data()

        actual_result = _test_executor.execute_test(test_data, "check_username_exists")

        self.assertFalse(actual_result)

    def test_get_all_users_returns_users_when_users_exist(self):

        test_data = test_get_all_users_returns_users_when_users_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_all_users")

        self.assertEqual(len(test_data.expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(test_data.expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(test_data.expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(test_data.expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(test_data.expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(test_data.expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(test_data.expected_result[i].manager, actual_result[i].manager)

    def test_get_all_users_returns_empty_list_when_users_do_not_exist(self):

        test_data = test_get_all_users_returns_empty_list_when_users_do_not_exist_data()

        actual_result = _test_executor.execute_test(test_data, "get_all_users")

        self.assertEqual(0, len(actual_result))

    def test_get_public_user_details_returns_user_details_when_user_exists(self):

        test_data = test_get_public_user_details_returns_user_details_when_user_exists_data()

        actual_result = _test_executor.execute_test(test_data, "get_public_user_details")

        self.assertEqual(test_data.expected_result.user_id, actual_result.user_id)
        self.assertEqual(test_data.expected_result.user_name, actual_result.user_name)
        self.assertEqual(test_data.expected_result.account_type, actual_result.account_type)
        self.assertEqual(test_data.expected_result.first_name, actual_result.first_name)
        self.assertEqual(test_data.expected_result.surname, actual_result.surname)
        self.assertEqual(test_data.expected_result.manager, actual_result.manager)

    def test_get_public_user_details_returns_none_when_user_does_not_exist(self):

        test_data = test_get_public_user_details_returns_none_when_user_does_not_exist()

        actual_result = _test_executor.execute_test(test_data, "get_public_user_details")

        self.assertEqual(None, actual_result)

    def test_update_user_password_not_updated_when_not_requested(self):

        test_data = test_update_user_password_not_updated_when_not_requested_data()

        # Method is void so cannot check output
        _test_executor.execute_test(test_data, "update_user")

    def test_update_user_password_updated_when_requested(self):

        test_data = test_update_user_password_updated_when_requested_data()

        # Method is void so cannot check output
        _test_executor.execute_test(test_data, "update_user")

    def test_update_user_projects_and_requests_updated_when_manager_changes(self):

        test_data = test_update_user_projects_and_requests_updated_when_manager_changes()

        # Method is void so cannot check output
        _test_executor.execute_test(test_data, "update_user")

    def test_delete_user_user_deleted_correctly_when_user_type_is_basic(self):

        test_data = test_delete_user_user_deleted_correctly_when_user_type_is_basic_data()

        # Method is void so cannot check output
        _test_executor.execute_test(test_data, "delete_user")

    def test_delete_user_user_deleted_correctly_when_user_type_is_manager(self):

        test_data = test_delete_user_user_deleted_correctly_when_user_type_is_manager_data()

        # Method is void so cannot check output
        _test_executor.execute_test(test_data, "delete_user")

    def test_delete_user_user_deleted_correctly_when_user_type_is_admin(self):

        test_data = test_delete_user_user_deleted_correctly_when_user_type_is_admin_data()

        # Method is void so cannot check output
        _test_executor.execute_test(test_data, "delete_user")
