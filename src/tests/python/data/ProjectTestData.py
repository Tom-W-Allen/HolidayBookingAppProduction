from datetime import datetime, date, timedelta

_current_date = datetime(date.today().year, date.today().month, date.today().day)

valid_test_start_date = datetime.strftime(_current_date + timedelta(10), "%Y-%m-%d")
valid_test_end_date = datetime.strftime(_current_date + timedelta(40), "%Y-%m-%d")

def find_project_name(x, y):
    return None

def find_project_name_exists(x, y):
    return "Test Project"

# <editor-fold desc="Test 1 Data">
def test_1_method_parameters():
    return [valid_test_start_date, valid_test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 2 Data">
def test_2_method_parameters():
    test_start_date = _current_date - timedelta(1)
    test_end_date = _current_date + timedelta(5)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    return [test_start_date, test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 3 Data">
def test_3_method_parameters():
    current_weekday = _current_date.isoweekday()
    # Find days from today to next Saturday
    advance = 7 - (current_weekday - 6) if current_weekday > 5 else 6 - current_weekday
    test_start_date = _current_date + timedelta(advance)
    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = _current_date + timedelta(advance + 1)
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    return [test_start_date, test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 4 Data">
def test_4_method_parameters():
    test_start_date = _current_date + timedelta(10)
    test_end_date = _current_date + timedelta(5)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    return [test_start_date, test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 5 Data">
def test_5_method_parameters():
    test_start_date = ""
    test_end_date = datetime.strftime(_current_date, "%Y-%m-%d")

    return [test_start_date, test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 6 Data">
def test_6_method_parameters():
    test_start_date = datetime.strftime(_current_date, "%Y-%m-%d")
    test_end_date = ""

    return [test_start_date, test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 7 Data">
def test_7_method_parameters():
    test_start_date = _current_date + timedelta(10)
    test_end_date = _current_date + timedelta(40)

    test_start_date = datetime.strftime(test_start_date, "%Y-%m-%d")
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    return [test_start_date, test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 8 Data">
def test_8_method_parameters():
    return ["Test Project", valid_test_start_date, valid_test_end_date, 5]

def test_8_query_strings():
    return ("SELECT project_id FROM projects ORDER BY project_id DESC",
            "SELECT project_id FROM employee_projects ORDER BY project_id DESC",
            "INSERT INTO projects VALUES (?, ?, ?, ?, ?)")

def test_8_mock_parameters():
    return (
        None,
        None,
        ["1", "Test Project", valid_test_start_date, valid_test_end_date, "5"]
    )

def test_8_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_8_query_strings()[0] and arguments == test_8_mock_parameters()[0] and limit == 1:
        return []
    elif query_string == test_8_query_strings()[1] and arguments == test_8_mock_parameters()[1] and limit == 1:
        return []
    elif query_string == test_8_query_strings()[2] and arguments == test_8_mock_parameters()[2] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 9 Data">
def test_9_method_parameters():
    return ["Test Project", valid_test_start_date, valid_test_end_date, 5]

def test_9_query_strings():
    return ("SELECT project_id FROM projects ORDER BY project_id DESC",
            "SELECT project_id FROM employee_projects ORDER BY project_id DESC",
            "INSERT INTO projects VALUES (?, ?, ?, ?, ?)")

def test_9_mock_parameters():
    return (
        None,
        None,
        ["11", "Test Project", valid_test_start_date, valid_test_end_date, "5"]
    )

def test_9_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_9_query_strings()[0] and arguments == test_9_mock_parameters()[0] and limit == 1:
        return [(10, None)]
    elif query_string == test_9_query_strings()[1] and arguments == test_9_mock_parameters()[1] and limit == 1:
        return [(5, None)]
    elif query_string == test_9_query_strings()[2] and arguments == test_9_mock_parameters()[2] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 10 Data">
def test_10_method_parameters():
    return ["Test Project", valid_test_start_date, valid_test_end_date, 5]

def test_10_query_strings():
    return ("SELECT project_id FROM projects ORDER BY project_id DESC",
            "SELECT project_id FROM employee_projects ORDER BY project_id DESC",
            "INSERT INTO projects VALUES (?, ?, ?, ?, ?)")

def test_10_mock_parameters():
    return (
        None,
        None,
        ["11", "Test Project", valid_test_start_date, valid_test_end_date, "5"]
    )

def test_10_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_10_query_strings()[0] and arguments == test_10_mock_parameters()[0] and limit == 1:
        return []
    elif query_string == test_10_query_strings()[1] and arguments == test_10_mock_parameters()[1] and limit == 1:
        return [(10, None)]
    elif query_string == test_10_query_strings()[2] and arguments == test_10_mock_parameters()[2] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 11 Data">
def test_11_query_strings():
    return "SELECT project_id, project_name, start_date, end_date, project_lead_id FROM projects"

def test_11_mock_parameters():
    return None

def test_11_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_11_query_strings() and arguments == test_11_mock_parameters() and limit is None:
        return [("1", "Test Name", "2020-5-30", "2021-5-30", "2"),
                ("2", "Test Name 2", "2020-5-30", "2021-5-30", "3")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 12 Data">
def test_12_method_parameters():
    test_end_date = _current_date + timedelta(5)
    test_end_date = datetime.strftime(test_end_date, "%Y-%m-%d")

    return [datetime.strftime(_current_date, "%Y-%m-%d"), test_end_date, "Test Project"]
# </editor-fold>

# <editor-fold desc="Test 13 Data">
def test_13_query_strings():
    return "SELECT project_id, project_name, start_date, end_date, project_lead_id FROM projects"

def test_13_mock_parameters():
    return None

def test_13_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_13_query_strings() and arguments == test_13_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 14 Data">
def test_14_method_parameters():
    return [2]

def test_14_query_strings():
    return "SELECT project_id, project_name, start_date, end_date FROM projects WHERE project_lead_id = ?"

def test_14_mock_parameters():
    return ["2"]

def test_14_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_14_query_strings() and arguments == test_14_mock_parameters() and limit is None:
        return [("1", "Test Name", "2020-5-30", "2021-5-30", "2"),
                ("2", "Test Name 2", "2020-5-30", "2021-5-30", "2")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 15 Data">
def test_15_method_parameters():
    return [2]

def test_15_query_strings():
    return "SELECT project_id, project_name, start_date, end_date FROM projects WHERE project_lead_id = ?"

def test_15_mock_parameters():
    return ["2"]

def test_15_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_15_query_strings() and arguments == test_15_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 16 Data">
def test_16_method_parameters():
    return [2]

def test_16_query_strings():
    return ("SELECT projects.project_id, projects.project_name, "
            "projects.start_date, projects.end_date, projects.project_lead_id "
            "FROM projects "
            "JOIN employee_projects ON "
            "projects.project_id = employee_projects.project_id "
            "WHERE employee_projects.employee_id = ? AND "
            "employee_projects.leave_date > ?")

def test_16_mock_parameters():
    return ["2", datetime.strftime(_current_date, "%Y-%m-%d")]

def test_16_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_16_query_strings() and arguments == test_16_mock_parameters() and limit is None:
        return [("1", "Test Name", "2020-5-30", "2021-5-30", "2"),
                ("2", "Test Name 2", "2020-5-30", "2021-5-30", "2")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 17 Data">
def test_17_method_parameters():
    return [2]

def test_17_query_strings():
    return ("SELECT projects.project_id, projects.project_name, "
            "projects.start_date, projects.end_date, projects.project_lead_id "
            "FROM projects "
            "JOIN employee_projects ON "
            "projects.project_id = employee_projects.project_id "
            "WHERE employee_projects.employee_id = ? AND "
            "employee_projects.leave_date > ?")

def test_17_mock_parameters():
    return ["2", datetime.strftime(_current_date, "%Y-%m-%d")]

def test_17_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_16_query_strings() and arguments == test_16_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 18 Data">
def test_18_method_parameters():
    return [1, 2]

def test_18_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname, manager, email_address "
            "FROM users AS u1 "
            "WHERE "
            "manager = ? AND "
            "NOT EXISTS (SELECT * FROM employee_projects WHERE "
            "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)")

def test_18_mock_parameters():
    return ["2", "1", datetime.strftime(_current_date, "%Y-%m-%d")]

def test_18_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_18_query_strings() and arguments == test_18_mock_parameters() and limit is None:
        return [("1", "Test Username", "basic", "Test Name", "Test Surname", "2", "Test Email"),
                ("3", "Test Username", "basic", "Test Name", "Test Surname", "2", "Test Email")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 19 Data">
def test_19_method_parameters():
    return [1, 2]

def test_19_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname, manager, email_address "
            "FROM users AS u1 "
            "WHERE "
            "manager = ? AND "
            "NOT EXISTS (SELECT * FROM employee_projects WHERE "
            "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)")

def test_19_mock_parameters():
    return ["2", "1", datetime.strftime(_current_date, "%Y-%m-%d")]

def test_19_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_19_query_strings() and arguments == test_19_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 20 Data">
def test_20_get_project_overlap_holidays(self, employee_id, project_id):
    if employee_id == 1 and project_id == 1:
        return [datetime(2020, 5, 10), datetime(2020, 6, 8)]
    elif employee_id == 3 and project_id == 1:
        return [datetime(2020, 5, 7)]
    else:
        raise Exception("Unexpected get project overlap query")

def test_20_method_parameters():
    return [1, 2]

def test_20_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname "
            "FROM users AS u1 "
            "WHERE "
            "manager = ? AND "
            "EXISTS (SELECT * FROM employee_projects WHERE "
            "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)")

def test_20_mock_parameters():
    return ["2", "1", datetime.strftime(_current_date, "%Y-%m-%d")]

def test_20_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_20_query_strings() and arguments == test_20_mock_parameters() and limit is None:
        return [(1, "Test Username", "basic", "Test Name", "Test Surname"),
                (3, "Test Username", "basic", "Test Name", "Test Surname")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 21 Data">
def test_21_get_project_overlap_holidays(self, employee_id, project_id):
    raise Exception("Unexpected get project overlap query")

def test_21_method_parameters():
    return [1, 2]

def test_21_query_strings():
    return ("SELECT user_id, user_name, user_role, first_name, surname "
            "FROM users AS u1 "
            "WHERE "
            "manager = ? AND "
            "EXISTS (SELECT * FROM employee_projects WHERE "
            "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)")

def test_21_mock_parameters():
    return ["2", "1", datetime.strftime(_current_date, "%Y-%m-%d")]

def test_21_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_21_query_strings() and arguments == test_21_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 22 Data">
def test_22_method_parameters():
    return [1, 2]

def test_22_query_strings():
    return ["SELECT start_date, end_date FROM projects WHERE project_id = ?",
            "SELECT * FROM employee_projects WHERE employee_id = ? AND project_id = ?",
            "INSERT INTO employee_projects VALUES (?, ?, ? ,?)"]

def test_22_mock_parameters():
    return [["2"],
            ["1", "2"],
            ["2", "1", "2020-5-10", "2020-6-10"]]

def test_22_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_22_query_strings()[0] and arguments == test_22_mock_parameters()[0] and limit is None:
        return [("2020-5-10", "2020-6-10")]
    elif query_string == test_22_query_strings()[1] and arguments == test_22_mock_parameters()[1] and limit is None:
        return []
    elif query_string == test_22_query_strings()[2] and arguments == test_22_mock_parameters()[2] and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 23 Data">
def test_23_method_parameters():
    return [1, 2]

def test_23_query_strings():
    return ["SELECT start_date, end_date FROM projects WHERE project_id = ?",
            "SELECT * FROM employee_projects WHERE employee_id = ? AND project_id = ?",
            "UPDATE employee_projects SET join_date = ?, leave_date = ? WHERE employee_id = ? AND project_id = ?"]

def test_23_mock_parameters():
    return [["2"],
            ["1", "2"],
            [datetime.strftime(_current_date, "%Y-%m-%d"), "2020-6-10", "1", "2"]]

def test_23_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_23_query_strings()[0] and arguments == test_23_mock_parameters()[0] and limit is None:
        return [("2020-5-10", "2020-6-10")]
    elif query_string == test_23_query_strings()[1] and arguments == test_23_mock_parameters()[1] and limit is None:
        return ["Preexisting Record"]
    elif query_string == test_23_query_strings()[2] and arguments == test_23_mock_parameters()[2] and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 24 Data">
def test_24_method_parameters():
    return [1, 2]

def test_24_query_strings():
    return "UPDATE employee_projects SET leave_date = ? WHERE employee_id = ? AND project_id = ?"

def test_24_mock_parameters():
    return [datetime.strftime(_current_date, "%Y-%m-%d"), "1", "2"]

def test_24_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_24_query_strings() and arguments == test_24_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 25 Data">
def test_25_method_parameters():
    return ["Test Project Name"]

def test_25_query_strings():
    return "SELECT * FROM projects WHERE project_name = ? LIMIT 1"

def test_25_mock_parameters():
    return ["Test Project Name"]

def test_25_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_25_query_strings() and arguments == test_25_mock_parameters() and limit is None:
        return ["Test Project Name"]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 26 Data">
def test_26_method_parameters():
    return ["Test Project Name"]

def test_26_query_strings():
    return "SELECT * FROM projects WHERE project_name = ? LIMIT 1"

def test_26_mock_parameters():
    return ["Test Project Name"]

def test_26_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_26_query_strings() and arguments == test_26_mock_parameters() and limit is None:
        return []
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 27 Data">
def test_27_method_parameters():
    return [1, 2]

def test_27_query_strings():
    return ["SELECT start_date, end_date FROM projects WHERE project_id = ?",
            "SELECT start_date, end_date FROM requests WHERE employee_id = ? AND request_status = 'approved'"]

def test_27_mock_parameters():
    return [["2"],
            ["1"]]

def test_27_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_27_query_strings()[0] and arguments == test_27_mock_parameters()[0] and limit == 1:
        return [("2020-4-1", "2020-6-1")]
    if query_string == test_27_query_strings()[1] and arguments == test_27_mock_parameters()[1] and limit is None:
        return [("2020-5-10", "2020-5-11")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 28 Data">
def test_28_method_parameters():
    return [1, 2]

def test_28_query_strings():
    return ["SELECT start_date, end_date FROM projects WHERE project_id = ?",
            "SELECT start_date, end_date FROM requests WHERE employee_id = ? AND request_status = 'approved'"]

def test_28_mock_parameters():
    return [["2"],
            ["1"]]

def test_28_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_27_query_strings()[0] and arguments == test_27_mock_parameters()[0] and limit == 1:
        return [("2020-4-1", "2020-6-1")]
    if query_string == test_27_query_strings()[1] and arguments == test_27_mock_parameters()[1] and limit is None:
        return [("2020-12-10", "2020-12-11")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>
