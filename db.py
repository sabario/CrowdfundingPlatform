import os
import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()
DB_FILE_PATH = os.getenv('DATABASE_URL')

def establish_db_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        print("Connection established: SQLite version", sqlite3.version)
    except Error as e:
        print(f"Database connection failed: {e}")
    return connection

def execute_sql_command(connection, sql_command):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()
    except Error as e:
        print(f"Failed to execute SQL command: {e}")

def initialize_database():
    db_path = DB_FILE_PATH

    sql_campaigns_table_creation = """ CREATE TABLE IF NOT EXISTS campaigns (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        description TEXT,
                                        goal_amount REAL NOT NULL,
                                        funded_amount REAL NOT NULL,
                                        start_date TEXT,
                                        end_date TEXT
                                    ); """

    connection = establish_db_connection(db_path)

    if connection is not None:
        execute_sql_command(connection, sql_campaigns_table_creation)
    else:
        print("Error! Cannot establish database connection.")

def insert_new_campaign(connection, campaign_data):
    sql_insert_campaign = ''' INSERT INTO campaigns(name, description, goal_amount, funded_amount, start_date, end_date)
                              VALUES(?,?,?,?,?,?) '''
    try:
        cursor = connection.cursor()
        cursor.execute(sql_insert_campaign, campaign_data)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting new campaign: {e}")
        return None

def modify_campaign_details(connection, updated_campaign_data):
    sql_update_campaign = ''' UPDATE campaigns
                              SET name = ?,
                                  description = ?,
                                  goal_amount = ?,
                                  funded_amount = ?,
                                  start_date = ?,
                                  end_date = ?
                              WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql_update_campaign, updated_campaign_data)
        connection.commit()
    except Error as e:
        print(f"Error updating campaign: {e}")

def retrieve_all_campaigns(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns")

        campaign_rows = cursor.fetchall()

        for campaign in campaign_rows:
            print(campaign)
    except Error as e:
        print(f"Error retrieving campaigns: {e}")

def retrieve_campaign_by_id(connection, campaign_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE id=?", (campaign_id,))

        campaign_details = cursor.fetchone()

        if campaign_details:
            print(campaign_details)
        else:
            print("Campaign not found.")
    except Error as e:
        print(f"Error retrieving campaign by ID: {e}")

if __name__ == '__main__':
    initialize_database()