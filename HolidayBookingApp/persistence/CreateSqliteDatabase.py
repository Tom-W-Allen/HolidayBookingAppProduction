import sqlite3 as database


def set_up_sqlite_database():

    with open("persistence/scripts/Holiday App Database Creation Script.sql", "r") as file:
        script = file.read()
        with database.connect("persistence/HolidayBookingDatabase.db") as connection:

            connection.cursor().executescript(script)

    with open("persistence/scripts/Holiday App Database Population Script.sql", "r") as file:
        script = file.read()
        with database.connect("persistence/HolidayBookingDatabase.db") as connection:

            connection.cursor().executescript(script)
