from HolidayBookingApp.tests.common.models.TestData import TestData
from HolidayBookingApp.common.enums.UserType import UserType
from HolidayBookingApp.domains.user.models.PublicUser import PublicUser
from HolidayBookingApp.domains.user.models.UserLoginData import UserLoginData
from datetime import datetime


# <editor-fold desc="Test 1 Data">
def test_1_method_parameters():
    return ["Test user name", "Test password", UserType.basic, "Test first name", "Test surname", 25, 2, "Test email"]

def test_1_query_strings():
    return ("SELECT user_id FROM users ORDER BY user_id DESC",
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

def test_1_mock_parameters():
    return (
        None,
        ["1", "Test user name", "Test password", None, str(UserType.basic),"Test first name", "Test surname", "2",
         "Test email", None, None, None, "25", "0"]
    )

def test_1_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_1_query_strings()[0] and arguments == test_1_mock_parameters()[0] and limit == 1:
        return []
    elif query_string == test_1_query_strings()[1] and arguments == test_1_mock_parameters()[1] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>


# <editor-fold desc="Test 2 Data">
def test_2_method_parameters():
    return ["Test user name", "Test password", UserType.basic, "Test first name", "Test surname", 25, 2, "Test email"]

def test_2_query_strings():
    return ("SELECT user_id FROM users ORDER BY user_id DESC",
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

def test_2_mock_parameters():
    return (
        None,
        ["2", "Test user name", "Test password", None, str(UserType.basic),"Test first name", "Test surname", "2",
         "Test email", None, None, None, "25", "0"]
    )

def test_2_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_2_query_strings()[0] and arguments == test_2_mock_parameters()[0] and limit == 1:
        return [(1, None)]
    elif query_string == test_2_query_strings()[1] and arguments == test_2_mock_parameters()[1] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>


##########################################################################################################

def test_add_user_sets_id_as_1_when_no_users_in_database_data():

    method_parameters = ["Test user name", "Test password", str(UserType.basic),
                         "Test first name", "Test surname", None, "25"]
    method_query_order = ["SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1",
                          "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"]
    expected_values = [[]]
    expected_parameters = [None,
                           ['1', "Test user name", "Test password", None, str(UserType.basic), "Test first name",
                            "Test surname", "25", "None"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_add_user_increments_id_when_users_already_exist_data():
    method_parameters = ["Test user name", "Test password", str(UserType.basic),
                         "Test first name", "Test surname", "1", "25"]
    method_query_order = ["SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1",
                          "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"]
    expected_values = [[['5']]]
    expected_parameters = [None,
                           ['6', "Test user name", "Test password", None, str(UserType.basic), "Test first name",
                            "Test surname", "25", "1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_add_user_manager_id_set_when_not_none_data():
    method_parameters = ["Test user name", "Test password", str(UserType.basic),
                         "Test first name", "Test surname", '1', "25"]
    method_query_order = ["SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1",
                          "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"]
    expected_values = [[['5']]]
    expected_parameters = [None,
                           ['6', "Test user name", "Test password", None, str(UserType.basic), "Test first name",
                            "Test surname", "25", '1']]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_get_user_manager_id_returned_when_manager_exists_data():
    method_parameters = ["5"]
    method_query_order = ["SELECT manager FROM users WHERE user_id = ? LIMIT 1"]
    expected_values = [[['10']]]
    expected_parameters = [["5"]]
    expected_result = '10'

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_user_negative_1_returned_when_manager_does_not_exist_data():
    method_parameters = ["5"]
    method_query_order = ["SELECT manager FROM users WHERE user_id = ? LIMIT 1"]
    expected_values = [[]]
    expected_parameters = [["5"]]
    expected_result = -1

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_user_type_details_empty_list_returned_when_no_users_exist_data():
    method_parameters = [UserType.manager]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname, "
                          "manager FROM users WHERE user_role = ?"]
    expected_values = [[]]
    expected_parameters = [[str(UserType.manager.name)]]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_user_type_details_list_returned_when_users_exist_data():
    method_parameters = [UserType.manager]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname, "
                          "manager FROM users WHERE user_role = ?"]
    expected_values = [[[1, "Test User Name", "manager", "Test First Name", "Test Surname", "None"],
                        [2, "Test User Name 2", "manager", "Test First Name 2", "Test Surname 2", "None"]]]
    expected_parameters = [[str(UserType.manager.name)]]
    expected_result = [PublicUser(1,
                                  "Test User Name",
                                  'manager',
                                  "Test First Name",
                                  "Test Surname",
                                  None),
                       PublicUser(2,
                                  "Test User Name 2",
                                  'manager',
                                  "Test First Name 2",
                                  "Test Surname 2",
                                  None)]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_user_login_details_none_returned_when_no_user_exists_data():
    method_parameters = ["Test user name"]
    method_query_order = ["SELECT user_id, user_password, user_role FROM users WHERE user_name = ?"]
    expected_values = [[]]
    expected_parameters = [["Test user name"]]
    expected_result = None

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_user_login_details_details_returned_when_user_exists_data():
    method_parameters = ["Test user name"]
    method_query_order = ["SELECT user_id, user_password, user_role FROM users WHERE user_name = ?"]
    expected_values = [[[1, "Test Password", "manager"]]]
    expected_parameters = [["Test user name"]]
    expected_result = UserLoginData(1,
                                    "Test user name",
                                    "Test Password",
                                    UserType.manager)

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_check_username_exists_returns_True_if_user_exists_data():
    method_parameters = ["Test user name"]
    method_query_order = ["SELECT user_name FROM users WHERE user_name = ?"]
    expected_values = [[["Test user name"]]]
    expected_parameters = [["Test user name"]]
    expected_result = True

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_check_username_exists_returns_False_if_user_does_not_exist_data():
    method_parameters = ["Test user name"]
    method_query_order = ["SELECT user_name FROM users WHERE user_name = ?"]
    expected_values = [[]]
    expected_parameters = [["Test user name"]]
    expected_result = False

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_all_users_returns_users_when_users_exist_data():
    method_parameters = []
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname, manager FROM users"]
    expected_values = [[("1", "Test Username 1", "basic", "Test 1", "Test 1", "2"),
                        ("2", "Test Username 2", "manager", "Test 2", "Test 2", "None")]]
    expected_parameters = [[]]
    expected_result = [PublicUser("1",
                                  "Test Username 1",
                                  "basic",
                                  "Test 1",
                                  "Test 1",
                                  "2"),
                       PublicUser("2",
                                  "Test Username 2",
                                  "manager",
                                  "Test 2",
                                  "Test 2",
                                  "None")]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_all_users_returns_empty_list_when_users_do_not_exist_data():
    method_parameters = []
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, surname, manager FROM users"]
    expected_values = [[]]
    expected_parameters = [[]]
    expected_result = []

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_public_user_details_returns_user_details_when_user_exists_data():
    method_parameters = [1]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, "
                          "surname, manager FROM users WHERE user_id = ?"]
    expected_values = [[("1", "Test Username 1", "basic", "Test 1", "Test 1", "2")]]
    expected_parameters = [["1"]]
    expected_result = PublicUser("1",
                                 "Test Username 1",
                                 "basic",
                                 "Test 1",
                                 "Test 1",
                                 2)

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_get_public_user_details_returns_none_when_user_does_not_exist():
    method_parameters = [1]
    method_query_order = ["SELECT user_id, user_name, user_role, first_name, "
                          "surname, manager FROM users WHERE user_id = ?"]
    expected_values = [[]]
    expected_parameters = [["1"]]
    expected_result = None

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters,
                    expected_result)


def test_update_user_password_not_updated_when_not_requested_data():
    method_parameters = [PublicUser(1,
                                    "Test",
                                    "basic",
                                    "Test",
                                    "Test",
                                    2)]
    method_query_order = [
        "SELECT user_id, user_name, user_role, first_name, surname, manager FROM users WHERE user_id = ?",
        "UPDATE users SET first_name = ?, surname = ?, manager = ? WHERE user_id = ?"]
    expected_values = [[(1, "Test B", "basic", "Test B", "Test B", 2)],
                       []]
    expected_parameters = [
        ["1"],
        ["Test", "Test", "2", "1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_update_user_password_updated_when_requested_data():
    method_parameters = [PublicUser(1,
                                    "Test",
                                    "basic",
                                    "Test",
                                    "Test",
                                    2),
                         True]
    method_query_order = [
        "SELECT user_id, user_name, user_role, first_name, surname, manager FROM users WHERE user_id = ?",
        "UPDATE users SET first_name = ?, surname = ?, manager = ? WHERE user_id = ?",
        "SELECT password_change FROM users WHERE user_id = ?",
        "UPDATE users SET user_password = ?,password_change = NULL WHERE user_id = ?"]
    expected_values = [[(1, "Test B", "basic", "Test B", "Test B", 2)],
                       [[("test password")]]]
    expected_parameters = [
        ["1"],
        ["Test", "Test", "2", "1"],
        ["1"],
        ["test password", "1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_update_user_projects_and_requests_updated_when_manager_changes():
    today = datetime.now()
    string_today = datetime.strftime(today, "%Y-%m-%d")

    method_parameters = [PublicUser(1,
                                    "Test",
                                    "basic",
                                    "Test",
                                    "Test",
                                    2)]
    method_query_order = [
        "SELECT user_id, user_name, user_role, first_name, surname, manager FROM users WHERE user_id = ?",

        "UPDATE users SET first_name = ?, surname = ?, manager = ? WHERE user_id = ?",

        "UPDATE employee_projects SET leave_date = ? WHERE employee_id = ? AND project_id IN "
        "(SELECT project_id FROM projects WHERE project_lead_id = ?)",

        "UPDATE requests SET approver_id = ? WHERE employee_id = ? AND request_status = 'pending'"]

    expected_values = [[(1, "Test B", "basic", "Test B", "Test B", 3)],
                       [[("test password")]]]
    expected_parameters = [
        ["1"],
        ["Test", "Test", "2", "1"],
        [string_today, "1", "3"],
        ["2", "1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_delete_user_user_deleted_correctly_when_user_type_is_basic_data():
    method_parameters = [PublicUser(1,
                                    "Test",
                                    "basic",
                                    "Test",
                                    "Test",
                                    2)]
    method_query_order = ["DELETE FROM employee_projects WHERE employee_id = ?",
                          "DELETE FROM requests WHERE employee_id = ?",
                          "DELETE FROM users WHERE user_id = ?"]

    expected_values = []
    expected_parameters = [["1"],
                           ["1"],
                           ["1"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_delete_user_user_deleted_correctly_when_user_type_is_manager_data():
    method_parameters = [PublicUser(2,
                                    "Test",
                                    "manager",
                                    "Test",
                                    "Test",
                                    None)]
    method_query_order = ["DELETE FROM projects WHERE project_lead_id = ?",
                          "UPDATE requests SET approver_id = ? WHERE approver_id = ?",
                          "UPDATE users SET manager = NULL WHERE manager = ?",
                          "DELETE FROM users WHERE user_id = ?"]

    expected_values = []
    expected_parameters = [["2"],
                           ["None", "2"],
                           ["2"],
                           ["2"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)


def test_delete_user_user_deleted_correctly_when_user_type_is_admin_data():
    method_parameters = [PublicUser(3,
                                    "Test",
                                    "admin",
                                    "Test",
                                    "Test",
                                    None)]
    method_query_order = ["DELETE FROM users WHERE user_id = ?"]

    expected_values = []
    expected_parameters = [["3"]]

    return TestData(expected_values,
                    method_query_order,
                    expected_parameters,
                    method_parameters)

