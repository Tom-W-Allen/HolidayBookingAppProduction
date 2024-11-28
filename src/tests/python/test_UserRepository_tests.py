from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from domains.user.UserRepository import UserRepository
from UserTestData import *
from persistence.Database import Database

_database = MagicMock()
_sut = UserRepository(_database)

def mock_postgre_sql(self):
    return True

class UserRepositoryMethodTests(TestCase):

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_1_query_function)
    def test_add_user_sets_id_as_1_when_no_users_in_database(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_1_method_parameters()

        expected_result = None
        actual_result = sut.add_user(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_2_query_function)
    def test_add_user_increments_id_when_users_already_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_2_method_parameters()

        expected_result = None
        actual_result = sut.add_user(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_3_query_function)
    def test_add_user_manager_id_set_when_not_none(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_3_method_parameters()

        expected_result = None
        actual_result = sut.add_user(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_4_query_function)
    def test_get_user_manager_id_returned_when_manager_exists(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_4_method_parameters()

        expected_result = 1
        actual_result = sut.get_user_manager(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_5_query_function)
    def test_get_user_manager_negative_1_returned_when_manager_does_not_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_5_method_parameters()

        expected_result = -1
        actual_result = sut.get_user_manager(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_6_query_function)
    def test_get_user_type_details_empty_list_returned_when_no_users_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_6_method_parameters()

        expected_result = []
        actual_result = sut.get_user_type_details(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_7_query_function)
    def test_get_user_type_details_list_returned_when_users_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_7_method_parameters()

        expected_result = test_7_expected_result()
        actual_result = sut.get_user_type_details(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

        for i in range(0, len(expected_result)):
            self.assertEqual(expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(expected_result[i].account_type, actual_result[i].account_type)
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_8_query_function)
    def test_get_user_login_details_none_returned_when_no_user_exists(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_8_method_parameters()

        expected_result = None
        actual_result = sut.get_user_login_details(*[arg for arg in input_parameters])
        self.assertEqual(expected_result, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_9_query_function)
    def test_get_user_login_details_details_returned_when_user_exists(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_9_method_parameters()

        expected_result = test_9_expected_result()[0]
        actual_result = sut.get_user_login_details(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.user_id, actual_result.user_id)
        self.assertEqual(expected_result.user_name, actual_result.user_name)
        self.assertEqual(expected_result.password, actual_result.password)
        self.assertEqual(str(expected_result.user_role), str(actual_result.user_role))

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_10_query_function)
    def test_check_username_exists_returns_True_if_user_exists(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_10_method_parameters()

        actual_result = sut.check_username_exists(*[arg for arg in input_parameters])

        self.assertTrue(actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_11_query_function)
    def test_check_username_exists_returns_False_if_user_does_not_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_11_method_parameters()

        actual_result = sut.check_username_exists(*[arg for arg in input_parameters])

        self.assertFalse(actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_12_query_function)
    def test_get_all_users_returns_users_when_users_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)

        expected_result = test_12_expected_result()
        actual_result = sut.get_all_users()

        self.assertEqual(len(expected_result), len(actual_result))

        for i in range(0, len(actual_result)):
            self.assertEqual(expected_result[i].user_id, actual_result[i].user_id)
            self.assertEqual(expected_result[i].user_name, actual_result[i].user_name)
            self.assertEqual(str(expected_result[i].account_type), str(actual_result[i].account_type))
            self.assertEqual(expected_result[i].first_name, actual_result[i].first_name)
            self.assertEqual(expected_result[i].surname, actual_result[i].surname)
            self.assertEqual(expected_result[i].manager, actual_result[i].manager)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_13_query_function)
    def test_get_all_users_returns_empty_list_when_users_do_not_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)

        actual_result = sut.get_all_users()

        self.assertEqual(0, len(actual_result))

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_14_query_function)
    def test_get_public_user_details_returns_user_details_when_user_exists(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_14_method_parameters()

        expected_result = test_14_expected_result()[0]
        actual_result = sut.get_public_user_details(*[arg for arg in input_parameters])

        self.assertEqual(expected_result.user_id, actual_result.user_id)
        self.assertEqual(expected_result.user_name, actual_result.user_name)
        self.assertEqual(str(expected_result.account_type), str(actual_result.account_type))
        self.assertEqual(expected_result.first_name, actual_result.first_name)
        self.assertEqual(expected_result.surname, actual_result.surname)
        self.assertEqual(expected_result.manager, actual_result.manager)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(Database, "query_database", test_15_query_function)
    def test_get_public_user_details_returns_none_when_user_does_not_exist(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_15_method_parameters()

        actual_result = sut.get_public_user_details(*[arg for arg in input_parameters])

        self.assertEqual(None, actual_result)

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(UserRepository, "get_public_user_details", test_16_get_public_user_details)
    @patch.object(Database, "query_database", test_16_query_function)
    def test_update_user_password_not_updated_when_not_requested(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_16_method_parameters()

        sut.update_user(*[arg for arg in input_parameters])

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(UserRepository, "get_public_user_details", test_17_get_public_user_details)
    @patch.object(Database, "query_database", test_17_query_function)
    def test_update_user_password_updated_when_requested(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_17_method_parameters()

        sut.update_user(*[arg for arg in input_parameters])

    @patch.object(UserRepository, "is_postgreSQL", mock_postgre_sql)
    @patch.object(UserRepository, "get_public_user_details", test_18_get_public_user_details)
    @patch.object(Database, "query_database", test_18_query_function)
    def test_update_user_projects_and_requests_updated_when_manager_changes(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_18_method_parameters()

        sut.update_user(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_19_query_function)
    def test_delete_user_user_deleted_correctly_when_user_type_is_basic(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_19_method_parameters()

        sut.delete_user(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_20_query_function)
    def test_delete_user_user_deleted_correctly_when_user_type_is_manager(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_20_method_parameters()

        sut.delete_user(*[arg for arg in input_parameters])

    @patch.object(Database, "query_database", test_21_query_function)
    def test_delete_user_user_deleted_correctly_when_user_type_is_admin(self):

        mock_database = Database()
        sut = UserRepository(mock_database)
        input_parameters = test_21_method_parameters()

        sut.delete_user(*[arg for arg in input_parameters])


if __name__ == '__main__':
    main()