class Database:

    def __init__(self,
                 database_name = None,
                 host = None,
                 user = None,
                 password = None,
                 port = None,
                 connection_string = None):
        self.database_name = database_name
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connection_string = connection_string

    def _build_query(self, schema, query_string, limit=None, set_search_path=True):
        return ""

    def _executeQuery(self, query_string, arguments=None, limit=None):
        return ""

    def query_database(self, query_string, schema = "Common", arguments=None, limit=None, set_search_path=True):

        query = self._build_query(schema, query_string)

        return self._executeQuery(query, arguments)