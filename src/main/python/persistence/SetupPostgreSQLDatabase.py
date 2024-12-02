from persistence.Databases.PostgreSQLDatabase import PostgreSQLDatabase

def setup_postgresql_database(database: PostgreSQLDatabase):
    try:
        schema_exists = len(database.query_database("SELECT * FROM information_schema.schemata "
                                                    "WHERE schema_name = ?;",
                                                    arguments=["Common"],
                                                    set_search_path=False)) > 0
        if not schema_exists:

            # Create common schema
            database.query_database("CREATE SCHEMA Common;")

            # Run script to set up tables
            with open("src/main/python/persistence/scripts/Holiday App Database Creation Script.sql") as creation_script:
                script = creation_script.read()
                database.query_database(script)

            # Run script to populate tables
            with open("src/main/python/persistence/scripts/Holiday App Database Population Script.sql") as population_script:
                script = population_script.read()
                database.query_database(script)

    except Exception as e:
        print(f"An error occurred when running the script: {e}")
