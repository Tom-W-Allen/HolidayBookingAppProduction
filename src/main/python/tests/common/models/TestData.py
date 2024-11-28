class TestData:
    def __init__(self, expected_values, expected_queries, expected_parameters, method_parameters, expected_result=None):
        self.expected_values = expected_values
        self.expected_queries = expected_queries
        self.expected_parameters = expected_parameters
        self.method_parameters = method_parameters
        self.expected_result = expected_result
