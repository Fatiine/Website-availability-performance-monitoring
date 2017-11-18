import sqlite3


def create_tables(database_name):
    '''Creates the monitoring table where we're going to insert current data
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

def insert_values(database_name, table_name, val):
  '''Inserts the values : "val" into the table "table_name" in the database "database_name" '''
  
  # Database and cursor connection
  connection = sqlite3.connect(database_name, timeout=10)
  cursor = connection.cursor()

  if table_name == "monitoring_table":
      sql_command = "INSERT INTO monitoring_table VALUES ( ?, ?, ?, ?, ?)"

  elif table_name == "alerts_table":
      sql_command = "INSERT INTO alerts_table VALUES (? , ? , ? , ?, ?)"

  cursor.execute(sql_command, val)


  # Save the changes before closing
  connection.commit()
  connection.close()


def select_values(database_name, table_name, selectData):
  ''' Gets the values that verify the "selectData" from the table "table_name" in the database "database_name" '''
    # Database and cursor connection
  connection = sqlite3.connect(database_name, timeout=10)
  cursor = connection.cursor()

  if table_name == "monitoring_table":
      sql_command = "SELECT * FROM monitoring_table WHERE URL = ? AND timedate >= ?"
      cursor.execute(sql_command, selectData)
  elif table_name == "alerts_table":
      sql_command = "SELECT * FROM alerts_table WHERE URL = ?"
      cursor.execute(sql_command, selectData)

  return cursor.fetchall()

def drop_tables(database_name):
  '''Drops the database tables alerts_table and monitoring_tables '''
  # Database and cursor connection
  connection = sqlite3.connect(database_name, timeout=10)
  cursor = connection.cursor()

  # Drop the table monitoring_table
  cursor.execute("DROP TABLE IF EXISTS monitoring_table")

  # Drop the table alerts_table
  cursor.execute("DROP TABLE IF EXISTS alerts_table")

  # Save changes before closing
  connection.commit()
  connection.close()