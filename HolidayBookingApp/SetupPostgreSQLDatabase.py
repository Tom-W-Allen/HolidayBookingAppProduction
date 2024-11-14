import argparse
from persistence.Databases.PostgreSQLDatabase import PostgreSQLDatabase

try:
    parser = argparse.ArgumentParser(description="Sets up tables in postgreSQL database and populates them if they "
                                                 "are not already available")

    parser.add_argument("database_name")
    parser.add_argument("host")
    parser.add_argument("user")
    parser.add_argument("password")
    parser.add_argument("port")
    args = parser.parse_args()

    database_name = args.database_name
    host = args.host
    user = args.user
    password = args.password
    port = args.port

    database = PostgreSQLDatabase(database_name=database_name,
                                  host=host,
                                  user=user,
                                  password=password,
                                  port=port)

    schema_exists = len(database.query_database("SELECT * FROM information_schema.schemata "
                                                "WHERE schema_name = ?;",
                                                arguments=["Common"],
                                                set_search_path=False)) < 0

    if not schema_exists:

        # Create common schema
        print("No schema exists, creating one now.")
        database.query_database("CREATE SCHEMA Common;")

        # Run script to set up tables
        print("Setting up tables.")
        with open("persistence/scripts/Holiday App Database Creation Script.sql") as creation_script:
            script = creation_script.read()
            database.query_database(script)

        # Run script to populate tables
        print("Populating tables.")
        with open("persistence/scripts/Holiday App Database Population Script.sql") as population_script:
            script = population_script.read()
            database.query_database(script)
    else:
        print("Schema already exists: skipping steps.")
except:
    print("An error occurred when running the script")
