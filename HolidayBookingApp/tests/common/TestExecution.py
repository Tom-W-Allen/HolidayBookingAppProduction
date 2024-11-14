from HolidayBookingApp.tests.common.DatabaseMocking import SqlTracer, MockContext
from unittest import mock


class TestExecutor:

    def __init__(self, sut, class_under_test):
        self._sut = sut
        self._class_under_test = class_under_test
        self._tracer = None

    def execute_test(self, test_data, method_name):

        self._tracer = SqlTracer()

        mock_context = MockContext(self._tracer,
                                   test_data.expected_values,
                                   test_data.expected_queries,
                                   test_data.expected_parameters)

        # User reflection to store the method to be tested in the method object.
        method = getattr(self._sut, method_name)

        # Set the mock_context object as the return value of sqlite3.connect (database.connect) in the
        # class under test.
        with mock.patch(f'{self._class_under_test}.database.connect', return_value=mock_context):
            # Execute the method by unpacking all the test_data method_parameters via the * operator
            # (Python, 2024c, 6.15).
            return method(*[arg for arg in test_data.method_parameters])
