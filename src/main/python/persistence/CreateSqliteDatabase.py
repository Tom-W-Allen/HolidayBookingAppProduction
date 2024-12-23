import sqlite3 as database
import os


def set_up_sqlite_database():
    current_file_path = os.path.dirname(__file__).split("\\")
    script_file_path = ("\\".join(current_file_path[:len(current_file_path) - 4])) + "\\"

    with open(f"{script_file_path}Holiday_App_Database_Creation_Script.sql", "r") as file:
        script = file.read()
        with database.connect("persistence/HolidayBookingDatabase.db") as connection:

            connection.cursor().executescript(script)

    with open(f"{script_file_path}Holiday_App_Database_Population_Script.sql", "r") as file:
        script = file.read()
        with database.connect("persistence/HolidayBookingDatabase.db") as connection:

            connection.cursor().executescript(script)
