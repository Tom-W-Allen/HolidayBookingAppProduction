import sqlite3 as database
from persistence.Database import Database

class SqliteDatabase(Database):
    def __init__(self, connection_string):
        super().__init__(connection_string=connection_string)
        self.connection_string = connection_string

    def _build_query(self, schema, query_string, limit = None):
        if limit is None:
            return query_string
        else:
            # ensure that limit is an integer
            try:
                int(limit)
                limit = " LIMIT " + limit
            except:
                limit = ""

            return query_string + limit

    def _executeQuery(self, query_string, arguments=None):
        with(database.connect(self.connection_string) as connection):
            try:
                if arguments is None:
                    return connection.cursor().execute(query_string).fetchall()
                else:
                    return connection.cursor().execute(query_string, arguments).fetchall()
            except Exception as e:
                pass # Update, Insert, or Delete query: nothing to return