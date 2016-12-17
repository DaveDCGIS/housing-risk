import update_database





def drop_tables(database_choice):
    connect_str = update_database.database_management.get_connect_str(database_choice)
    engine = update_database.create_engine(connect_str)
    database_connection = engine.connect()
    query_result = database_connection.execute("DROP SCHEMA public CASCADE;CREATE SCHEMA public;")

if __name__ == '__main__':
    database_choice = 'database'
    drop_tables(database_choice)
    update_database.csv_to_sql(update_database.constants['manifest_filename'], database_choice)
