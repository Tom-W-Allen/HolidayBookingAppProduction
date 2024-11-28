# unittest is not by default capable of mocking the behaviour of internal libraries written in C (StackOverflow, 2008;
# StackOverflow, 2010). Since sqlite3 (Python 2024b) is one of these libraries, it is necessary to build a chain of
# objects that can simulate database calls.
class MockContext:
    def __init__(self, tracer, expected_values, expected_strings, optional_parameters=None):
        self._execution = MockExecution(expected_values)
        self._cursor = MockCursor(self._execution, tracer, expected_strings, optional_parameters)
        self._connection = MockConnection(self._cursor)
        self._tracer = tracer

    def __enter__(self):
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


class MockConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor


class MockCursor:
    def __init__(self, executor, tracer, expected_strings, optional_parameters=None):
        self._executor = executor
        self._tracer = tracer
        self._expected_string = expected_strings
        self._optional_parameters = [None for _ in range(0, len(expected_strings))] if optional_parameters is None \
            else optional_parameters
        self._count = 0

    def execute(self, string, parameters=None):
        if (string == self._expected_string[self._count] and
                (parameters is None and self._optional_parameters[0] == []) or
                (parameters == self._optional_parameters[self._count])):
            self._count += 1
            self._tracer.trace(string, parameters)
            return self._executor
        else:
            raise Exception(f"Parameter or query string mismatch found:\n "
                            f"expected string: {self._expected_string[self._count]}\n "
                            f"actual   string: {string}\n "
                            f"expected parameters: {self._optional_parameters[self._count]}\n "
                            f"actual   parameters: {parameters}")


class MockExecution:
    def __init__(self, value):
        self._value = value
        self._count = 0

    def fetchall(self):
        return_value = self._value[self._count]
        self._count += 1
        return return_value


class SqlTracer:
    def __init__(self):
        self.database_calls = []
        self.database_parameters = []

    def trace(self, query, parameters=None):
        self.database_calls.append(query)
        self.database_parameters.append(parameters)
