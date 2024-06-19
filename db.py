import os
import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()
DB_FILE_PATH = os.getenv('DATABASE_URL')

def establish_db_connection(db_path):
    try:
        connection = sqlite3.connect(db_path)
        print("Connection established: SQLite version", sqlite3.version)
    except Error as e:
        print(f"Database connection failed: {e}")
        connection = None
    return connection

def execute_sql_command(connection, sql_command, data=None, commit=True):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_command, data)
        else:
            cursor.execute(sql_command)
        if commit:
            connection.commit()
        return cursor
    except Error as e:
        print(f"Failed to execute SQL command: {e}")

def create_campaigns_table(connection):
    sql_command = '''CREATE TABLE IF NOT EXISTS campaigns (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        goal_amount REAL NOT NULL,
                        funded_amount REAL NOT NULL,
                        start_date TEXT,
                        end_date TEXT
                    );'''
    execute_sql_command(connection, sql_command)

def initialize_database():
    connection = establish_db_connection(DB_FILE_PATH)
    if connection:
        create_campaigns_table(connection)
    else:
        print("Error! Cannot establish database connection.")

def insert_new_campaign(connection, campaign_data):
    sql_command = '''INSERT INTO campaigns(name, description, goal_amount, funded_amount, start_date, end_date)
                     VALUES(?,?,?,?,?,?)'''
    cursor = execute_sql_command(connection, sql_command, campaign_data)
    return cursor.lastrowid if cursor else None

def modify_campaign_details(connection, updated_campaign_data):
    sql_command = '''UPDATE campaigns
                     SET name = ?, description = ?, goal_amount = ?, funded_amount = ?, start_date = ?, end_date = ?
                     WHERE id = ?'''
    execute_sql_command(connection, sql_command, updated_campaign_data)

def retrieve_all_campaigns(connection):
    cursor = execute_sql_command(connection, "SELECT * FROM campaigns", commit=False)
    if cursor:
        for campaign in cursor.fetchall():
            print(campaign)

def retrieve_campaign_by_id(connection, campaign_id):
    cursor = execute_sql_command(connection, "SELECT * FROM campaigns WHERE id=?", (campaign_id,), commit=False)
    campaign_details = cursor.fetchone() if cursor else None
    if campaign_details:
        print(campaign_details)
    else:
        print("Campaign not found.")

if __name__ == '__main__':
    initialize_database()