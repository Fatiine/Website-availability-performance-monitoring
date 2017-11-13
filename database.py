import sqlite3


def create_tables(database_name):
    '''Create the monitoring table where we're going to insert current data
    		the stats table where we're going to insert the stats we calculate every timeframe
    		the alerts table where we're going to insert alert and recovery data''' 

    # Initialize the database connection and the object cursor
    connection = sqlite3.connect(database_name, timeout=10)
    cursor = connection.cursor()

    # Create the montoring table
    sql_command = "CREATE TABLE IF NOT EXISTS " \
                  "monitoring_table (" \
                  "URL VARCHAR(100) ," \
                  "timedate VARCHAR(20)," \
                  " availability BIT," \
                  " status_code INT," \
                  " response_time FLOAT )"
    cursor.execute(sql_command)

    # Create the stats table
    sql_command = "CREATE TABLE IF NOT EXISTS " \
                  "stats_table (" \
                  "URL VARCHAR(100) ," \
                  "timedate VARCHAR(20)," \
                  "timeframe INT," \
                  " availability FLOAT," \
                  " status_code VARCHAR(100)," \
                  " max_RT FLOAT," \
                  " min_RT FLOAT," \
                  " avg_RT FLOAT)"
    cursor.execute(sql_command)

    # Create the alert table
    sql_command = "CREATE TABLE IF NOT EXISTS " \
                  "alerts_table (" \
                  "URL VARCHAR(100) ," \
                  "timedate VARCHAR(20)," \
                  " availability FLOAT," \
                  " isDown BIT," \
                  " message VARCHAR(10) )"
    cursor.execute(sql_command)

    # Save the changes before closing
    connection.commit()
    connection.close()
    return

def insert_values(database_name, table, values):
    # Database and cursor connection
    connection = sqlite3.connect(database_name, timeout=10)
    cursor = connection.cursor()

    if table == "monitoring_table":
        sql_command = "INSERT INTO monitoring_table VALUES ( ?, ?, ?, ?, ?)"

    elif table == "stats_table":
        sql_command = "INSERT INTO stats_table VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"

    elif table == "alerts_table":
        sql_command = "INSERT INTO alerts_table VALUES (? , ? , ? , ?, ?)"
    
    cursor.execute(sql_command, values)


    # Save the changes before closing
    connection.commit()
    connection.close()


def select_values(database_name, table, selectData):
    # Database and cursor connection
    connection = sqlite3.connect(database_name, timeout=10)
    cursor = connection.cursor()

    if table == "monitoring_table":
        sql_command = "SELECT * FROM monitoring_table WHERE URL = ? AND timedate >= ?"
    cursor.execute(sql_command,selectData)

    return cursor.fetchall()