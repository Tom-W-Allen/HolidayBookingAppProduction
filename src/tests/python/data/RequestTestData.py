from common.enums.RequestStatus import RequestStatus

# <editor-fold desc="Test 1 Data">
def test_1_method_parameters():
    return ["2020-5-1", "2020-5-10", 1, 2, 5]

def test_1_query_strings():
    return ["SELECT request_id FROM requests ORDER BY request_id DESC",
            "INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)"]

def test_1_mock_parameters():
    return (
        None,
        ["1", "2020-5-1", "2020-5-10", "1", "2", "pending", "5"]
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
    return ["2020-5-1", "2020-5-10", 1, 2, 5]

def test_2_query_strings():
    return ["SELECT request_id FROM requests ORDER BY request_id DESC",
            "INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)"]

def test_2_mock_parameters():
    return (
        None,
        ["6", "2020-5-1", "2020-5-10", "1", "2", "pending", "5"]
    )

def test_2_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_2_query_strings()[0] and arguments == test_2_mock_parameters()[0] and limit == 1:
        return [("5", None)]
    elif query_string == test_2_query_strings()[1] and arguments == test_2_mock_parameters()[1] and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 3 Data">
def test_3_method_parameters():
    return [5]

def test_3_query_strings():
    return ("SELECT requests.request_id, users.first_name, users.surname, "
            "requests.start_date, requests.end_date, requests.total_holidays "
            "FROM requests "
            "JOIN users ON requests.employee_id = users.user_id "
            "WHERE requests.approver_id = ? AND "
            "requests.request_status = 'pending'")

def test_3_mock_parameters():
    return ["5"]

def test_3_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_3_query_strings() and arguments == test_3_mock_parameters() and limit is None:
        return [(10, "Test Name", "Test Surname", "2020-5-10", "2020-5-15", 5),
                (11, "Test Name", "Test Surname", "2020-6-10", "2020-6-16", 6)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 4 Data">
def test_4_method_parameters():
    return [5]

def test_4_query_strings():
    return ("SELECT request_id, users.first_name, users.surname, "
            "start_date, end_date, requests.total_holidays, "
            "requests.request_status "
            "FROM requests "
            "LEFT JOIN users ON requests.approver_id = users.user_id "
            "WHERE requests.employee_id = ? "
            "ORDER BY request_id DESC")

def test_4_mock_parameters():
    return ["5"]

def test_4_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_4_query_strings() and arguments == test_4_mock_parameters() and limit is None:
        return [(10, "Test Name", "Test Surname", "2020-7-10", "2020-7-15", 5, "pending"),
                (11, "Test Name", "Test Surname", "2020-8-10", "2020-8-16", 6, "approved")]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 5 Data">
def test_5_method_parameters():
    return [10]

def test_5_query_strings():
    return ["SELECT total_holidays, employee_id FROM requests WHERE request_id = ?",
            "UPDATE requests SET request_status = 'approved' WHERE request_id = ?",
            "UPDATE users SET holidays_remaining = holidays_remaining - ? WHERE user_id = ?"]

def test_5_mock_parameters():
    return (["10"],
            ["10"],
            ["5", "2"])

def test_5_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_5_query_strings()[0] and arguments == test_5_mock_parameters()[0] and limit is None:
        return [(5, 2)]
    elif query_string == test_5_query_strings()[1] and arguments == test_5_mock_parameters()[1] and limit is None:
        pass
    elif query_string == test_5_query_strings()[2] and arguments == test_5_mock_parameters()[2] and limit is None:
        pass
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 6 Data">
def test_6_method_parameters():
    return [5]

def test_6_query_strings():
    return "UPDATE requests SET request_status = 'rejected' WHERE request_id = ?"

def test_6_mock_parameters():
    return ["5"]

def test_6_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_6_query_strings() and arguments == test_6_mock_parameters() and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 7 Data">
def test_7_method_parameters():
    return [3]

def test_7_query_strings():
    return "UPDATE requests SET request_status = 'cancelled' WHERE request_id = ?"

def test_7_mock_parameters():
    return ["3"]

def test_7_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_7_query_strings() and arguments == test_7_mock_parameters() and limit is None:
        return None
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 8 Data">
def test_8_method_parameters():
    return [9]

def test_8_query_strings():
    return "SELECT SUM(total_holidays) FROM requests WHERE employee_id = ? AND request_status = 'pending'"

def test_8_mock_parameters():
    return ["9"]

def test_8_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_8_query_strings() and arguments == test_8_mock_parameters() and limit is None:
        return [(20, None)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 9 Data">
def test_9_method_parameters():
    return [11]

def test_9_query_strings():
    return "SELECT SUM(total_holidays) FROM requests WHERE employee_id = ? AND request_status = 'pending'"

def test_9_mock_parameters():
    return ["11"]

def test_9_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_9_query_strings() and arguments == test_9_mock_parameters() and limit is None:
        return [(None, None)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 10 Data">
def test_10_method_parameters():
    return [14]

def test_10_query_strings():
    return "SELECT * FROM requests WHERE employee_id = ? AND request_status IN ('approved', 'pending')"

def test_10_mock_parameters():
    return ["14"]

def test_10_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_10_query_strings() and arguments == test_10_mock_parameters() and limit is None:
        return [(1, "2020-3-10", "2020-3-12", 14, 3, "pending", 2),
                (2, "2019-3-10", "2019-3-12", 14, 3, "approved", 2)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>

# <editor-fold desc="Test 11 Data">
def test_11_method_parameters():
    return [RequestStatus.pending]

def test_11_query_strings():
    return "SELECT request_id, start_date, end_date FROM requests WHERE request_status = ?"

def test_11_mock_parameters():
    return ["pending"]

def test_11_query_function(self, query_string, arguments=None, limit=None):

    if query_string == test_11_query_strings() and arguments == test_11_mock_parameters() and limit is None:
        return [(1, "2021-3-10", "2021-3-12", 14, 3, "pending", 2),
                (2, "2020-3-10", "2020-3-12", 14, 3, "pending", 2)]
    else:
        raise Exception("Unexpected query")
# </editor-fold>
