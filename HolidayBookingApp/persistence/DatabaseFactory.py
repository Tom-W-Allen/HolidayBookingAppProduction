import os

from persistence.Databases.SqliteDatabase import SqliteDatabase
from persistence.Databases.PostgreSQLDatabase import PostgreSQLDatabase
from dotenv import load_dotenv

def get_database(variable):
    load_dotenv()

    database_name = os.getenv("DATABASE_NAME")
    host = os.getenv("HOST")
    user = os.getenv("USER")
    port = os.getenv("DATABASE_PORT")


    if not valid_postgres_config(database_name, host, user, port):
        return SqliteDatabase("persistence/HolidayBookingDatabase.db")
    else:
        return PostgreSQLDatabase(database_name,
                                  host,
                                  user,
                                  "", # Server uses an internal connection so no password
                                  port)


def valid_postgres_config(database_name, host, user, port):
    return None not in [database_name, host, user, port]
