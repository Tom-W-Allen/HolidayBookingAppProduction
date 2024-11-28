import psycopg2
from persistence.Database import Database

class PostgreSQLDatabase(Database):

    def __init__(self, database_name, host, user, password, port):
        super().__init__(database_name, host, user, password, port)
        self.database_name = database_name
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.type = "postgreSQL"

    def _build_connection(self):
        return psycopg2.connect(database=self.database_name,
                                host=self.host,
                                user=self.user,
                                password=self.password,
                                port=self.port)

    def _build_query(self, schema, query_string, limit=None, set_search_path=True):
        reformatted_query = str(query_string).replace("?", "%s")
        if set_search_path:
            return f"SET search_path TO {schema}; {reformatted_query}"
        else:
            return reformatted_query

    def _executeQuery(self, query_string, arguments=None, limit=None):
        connection = self._build_connection()
        cursor = connection.cursor()

        if arguments is None:
            cursor.execute(query_string)
        else:
            argument_tuple = tuple(arguments)
            cursor.execute(query_string, argument_tuple)

        try:
            if limit is None:
                return cursor.fetchall()
            else:
                parsed_limit = int(limit)
                return cursor.fetchmany(parsed_limit)
        except psycopg2.ProgrammingError:
            # No results to return, Insert or Delete query
            connection.commit()
        finally:
            cursor.close()
            connection.close()




