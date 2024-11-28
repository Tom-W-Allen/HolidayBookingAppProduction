from common.enums.UserType import UserType
from domains.user.models.PublicUser import PublicUser
from domains.user.models.UserLoginData import UserLoginData
from datetime import datetime


# <editor-fold desc="Test 1 Data">
def test_1_method_parameters():
    return ["Test user name", "Test password", UserType.basic, "Test first name", "Test surname", 25, None, "Test email"]

def test_1_query_strings():
    return ("SELECT user_id FROM users ORDER BY user_id DESC",
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

def test_1_mock_parameters():
    return (
        None,
        ["1", "Test user name", "Test password", None, str(UserType.basic),"Test first name", "Test surname", None,
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
    return ["Test user name", "Test password", UserType.basic, "Test first name", "Test surname", 25, None, "Test email"]

def test_2_query_strings():
    return ("SELECT user_id FROM users ORDER BY user_id DESC",
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

def test_2_mock_parameters():
    return (
        None,
        ["2", "Test user name", "Test password", None, str(UserType.basic),"Test first name", "Test surname", None,
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

# <editor-fold desc="Test 3 Data">
def test_3_method_parameters():
    return ["Test user name", "Test password", UserType.basic, "Test first name", "Test surname", 25, 2, "Test email"]

def test_3_query_strings():
    return ("SELECT user_id FROM users ORDER BY user_id DESC",
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

def test_3_mock_parameters():
    return (
        None,
        ["2", "Test user name", "Test password", None, str(UserType.basic),"Test first name", "Test surname", "2",
         "Test email", None, None, None, "25", "0"]
    )

def test_3_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_3_query_strings()[0] and arguments == test_3_mock_parameters()[0] and limit == 1:
        return [(1, None)]
    elif query_string == test_3_query_strings()[1] and arguments == test_3_mock_parameters()[1] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 4 Data">
def test_4_method_parameters():
    return [5]

def test_4_query_strings():
    return "SELECT manager FROM users WHERE user_id = ?"

def test_4_mock_parameters():
    return ["5"]

def test_4_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_4_query_strings() and arguments == test_4_mock_parameters() and limit == 1:
        return [(1, None)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 5 Data">
def test_5_method_parameters():
    return [5]

def test_5_query_strings():
    return "SELECT manager FROM users WHERE user_id = ?"

def test_5_mock_parameters():
    return ["5"]

def test_5_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_5_query_strings() and arguments == test_5_mock_parameters() and limit == 1:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 6 Data">
def test_6_method_parameters():
    return [UserType.admin]

def test_6_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname, manager, "
            "email_address FROM users WHERE user_role = ?")

def test_6_mock_parameters():
    return ["admin"]

def test_6_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_6_query_strings() and arguments == test_6_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 7 Data">
def test_7_method_parameters():
    return [UserType.admin]

def test_7_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname, manager, "
            "email_address FROM users WHERE user_role = ?")

def test_7_mock_parameters():
    return ["admin"]

def test_7_expected_result() -> [PublicUser]:
    return [PublicUser(1, "Test", "admin", "Test First Name",
                       "Test Surname", None, "Test Email")]

def test_7_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_7_query_strings() and arguments == test_7_mock_parameters() and limit is None:
        result = test_7_expected_result()[0]
        return [(result.user_id, result.user_name, result.account_type, result.first_name,
                 result.surname, result.manager, result.email)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 8 Data">
def test_8_method_parameters():
    return ["Test User Name"]

def test_8_query_strings():
    return "SELECT user_id, user_password, user_role, password_attempts FROM users WHERE user_name = ?"

def test_8_mock_parameters():
    return ["Test User Name"]

def test_8_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_8_query_strings() and arguments == test_8_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 9 Data">
def test_9_method_parameters():
    return ["Test User Name"]

def test_9_query_strings():
    return "SELECT user_id, user_password, user_role, password_attempts FROM users WHERE user_name = ?"

def test_9_mock_parameters():
    return ["Test User Name"]

def test_9_expected_result() -> [UserLoginData]:
    return [UserLoginData(1, "Test User Name",
                          "Test Password", UserType.admin, 0)]

def test_9_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_9_query_strings() and arguments == test_9_mock_parameters() and limit is None:
        result = test_9_expected_result()[0]
        return [(result.user_id, result.password, "admin", result.password_attempts)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 10 Data">
def test_10_method_parameters():
    return ["Test User Name"]

def test_10_query_strings():
    return "SELECT user_name FROM users WHERE user_name = ?"

def test_10_mock_parameters():
    return ["Test User Name"]

def test_10_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_10_query_strings() and arguments == test_10_mock_parameters() and limit is None:
        return [("Test User Name", None)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 11 Data">
def test_11_method_parameters():
    return ["Test User Name"]

def test_11_query_strings():
    return "SELECT user_name FROM users WHERE user_name = ?"

def test_11_mock_parameters():
    return ["Test User Name"]

def test_11_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_11_query_strings() and arguments == test_11_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 12 Data">
def test_12_query_strings():
    return "SELECT user_id, user_name, user_role, first_name, surname, manager, email_address FROM users"

def test_12_expected_result():
    return[PublicUser(1, "Test User Name", "basic", "Test First Name",
                      "Test Surname", 2, "Test Email")]

def test_12_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_12_query_strings() and arguments is None and limit is None:
        result = test_12_expected_result()[0]
        return [(result.user_id, result.user_name, "basic", result.first_name,
                 result.surname, result.manager, result.email)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 13 Data">
def test_13_query_strings():
    return "SELECT user_id, user_name, user_role, first_name, surname, manager, email_address FROM users"

def test_13_expected_result():
    return[PublicUser(1, "Test User Name", "basic", "Test First Name",
                      "Test Surname", 2, "Test Email")]

def test_13_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_12_query_strings() and arguments is None and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 14 Data">
def test_14_method_parameters():
    return ["1"]

def test_14_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname, manager, "
            "email_address FROM users WHERE user_id = ?")

def test_14_mock_parameters():
    return ["1"]

def test_14_expected_result() -> [UserLoginData]:
    return [PublicUser(1, "Test User Name", "basic", "Test First Name",
                       "Test Surname", 5, "Test Email")]

def test_14_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_14_query_strings() and arguments == test_14_mock_parameters() and limit is None:
        result = test_14_expected_result()[0]
        return [(result.user_id, result.user_name, "basic", result.first_name, result.surname,
                 result.manager, result.email)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 15 Data">
def test_15_method_parameters():
    return ["1"]

def test_15_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname, manager, "
            "email_address FROM users WHERE user_id = ?")

def test_15_mock_parameters():
    return ["1"]

def test_15_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_15_query_strings() and arguments == test_15_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 16 Data">
def test_16_get_public_user_details(self, x):
    return PublicUser(1, "Test User Name", "manager", "Test Name",
                       "Test Surname", None, "Test Email")

def test_16_method_parameters():
    return [PublicUser(1, "Test User Name", "manager", "Test Name",
                       "Test Surname", None, "Test Email")]

def test_16_query_strings():
    return "UPDATE users SET first_name = ?, surname = ?, manager = ?, email_address = ? WHERE user_id = ?"

def test_16_mock_parameters():
    inputs = test_16_method_parameters()[0]
    return [inputs.first_name, inputs.surname, None, inputs.email, str(inputs.user_id)]

def test_16_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_16_query_strings() and arguments == test_16_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 17 Data">
def test_17_get_public_user_details(self, x):
    return PublicUser(1, "Test User Name", "manager", "Test Name",
                       "Test Surname", None, "Test Email")

def test_17_method_parameters():
    return [PublicUser(1, "Test User Name", "manager", "Test Name",
                       "Test Surname", None, "Test Email"), True]

def test_17_query_strings():
    return ("UPDATE users SET first_name = ?, surname = ?, manager = ?, email_address = ? WHERE user_id = ?",
            "SELECT password_change FROM users WHERE user_id = ?",
            "UPDATE users SET user_password = ?,password_change = NULL WHERE user_id = ?")

def test_17_mock_parameters():
    inputs = test_17_method_parameters()[0]
    return [[inputs.first_name, inputs.surname, None, inputs.email, str(inputs.user_id)],
            [str(inputs.user_id)],
            ["Test New Password", str(inputs.user_id)]]

def test_17_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_17_query_strings()[0] and arguments == test_17_mock_parameters()[0] and limit is None:
        return []
    elif query_string == test_17_query_strings()[1] and arguments == test_17_mock_parameters()[1] and limit is None:
        return [("Test New Password", None)]
    elif query_string == test_17_query_strings()[2] and arguments == test_17_mock_parameters()[2] and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 18 Data">
def test_18_get_public_user_details(self, x):
    return PublicUser(1, "Test User Name", "basic", "Test Name",
                       "Test Surname", 6, "Test Email")

def test_18_method_parameters():
    return [PublicUser(1, "Test User Name", "basic", "Test Name",
                       "Test Surname", 5, "Test Email"), True]

def test_18_query_strings():
    return ("UPDATE users SET first_name = ?, surname = ?, manager = ?, email_address = ? WHERE user_id = ?",
            "SELECT password_change FROM users WHERE user_id = ?",
            "UPDATE users SET user_password = ?,password_change = NULL WHERE user_id = ?",
            "UPDATE employee_projects SET leave_date = ? WHERE employee_id = ? AND project_id IN "
            "(SELECT project_id FROM projects WHERE project_lead_id = ?)",
            "UPDATE requests SET approver_id = ? WHERE employee_id = ? AND request_status = 'pending'"
            )

def test_18_mock_parameters():
    inputs = test_18_method_parameters()[0]
    today = datetime.now()
    string_today = datetime.strftime(today, "%Y-%m-%d")

    return [[inputs.first_name, inputs.surname, str(inputs.manager), inputs.email, str(inputs.user_id)],
            [str(inputs.user_id)],
            ["Test New Password", str(inputs.user_id)],
            [string_today, str(inputs.user_id), "6"],
            [str(inputs.manager), str(inputs.user_id)]]

def test_18_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_18_query_strings()[0] and arguments == test_18_mock_parameters()[0] and limit is None:
        return []
    elif query_string == test_18_query_strings()[1] and arguments == test_18_mock_parameters()[1] and limit is None:
        return [("Test New Password", None)]
    elif query_string == test_18_query_strings()[2] and arguments == test_18_mock_parameters()[2] and limit is None:
        return []
    elif query_string == test_18_query_strings()[3] and arguments == test_18_mock_parameters()[3] and limit is None:
        return []
    elif query_string == test_18_query_strings()[4] and arguments == test_18_mock_parameters()[4] and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 19 Data">
def test_19_method_parameters():
    return [PublicUser(1, "Test User Name", "basic", "Test Name",
                       "Test Surname", 5, "Test Email")]

def test_19_query_strings():
    return ("DELETE FROM employee_projects WHERE employee_id = ?",
            "DELETE FROM requests WHERE employee_id = ?",
            "DELETE FROM users WHERE user_id = ?"
            )

def test_19_mock_parameters():
    inputs = test_19_method_parameters()[0]

    return [str(inputs.user_id)]

def test_19_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_19_query_strings()[0] and arguments == test_19_mock_parameters() and limit is None:
        return []
    elif query_string == test_19_query_strings()[1] and arguments == test_19_mock_parameters() and limit is None:
        return [("Test New Password", None)]
    elif query_string == test_19_query_strings()[2] and arguments == test_19_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 20 Data">
def test_20_method_parameters():
    return [PublicUser(1, "Test User Name", "manager", "Test Name",
                       "Test Surname", None, "Test Email")]

def test_20_query_strings():
    return ("DELETE FROM projects WHERE project_lead_id = ?",
            "UPDATE requests SET approver_id = ? WHERE approver_id = ?",
            "UPDATE users SET manager = NULL WHERE manager = ?",
            "DELETE FROM users WHERE user_id = ?"
            )

def test_20_mock_parameters():
    inputs = test_19_method_parameters()[0]

    return [[str(inputs.user_id)],
            [str(None), str(inputs.user_id)],
            [str(inputs.user_id)],
            [str(inputs.user_id)]]

def test_20_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_20_query_strings()[0] and arguments == test_20_mock_parameters()[0] and limit is None:
        return []
    elif query_string == test_20_query_strings()[1] and arguments == test_20_mock_parameters()[1] and limit is None:
        return [("Test New Password", None)]
    elif query_string == test_20_query_strings()[2] and arguments == test_20_mock_parameters()[2] and limit is None:
        return []
    elif query_string == test_20_query_strings()[3] and arguments == test_20_mock_parameters()[3] and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 21 Data">
def test_21_method_parameters():
    return [PublicUser(1, "Test User Name", "admin", "Test Name",
                       "Test Surname", None, "Test Email")]

def test_21_query_strings():
    return "DELETE FROM users WHERE user_id = ?"

def test_21_mock_parameters():
    inputs = test_19_method_parameters()[0]

    return [str(inputs.user_id)]

def test_21_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_21_query_strings() and arguments == test_21_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>
