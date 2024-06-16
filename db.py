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
        print(e)
    return connection

def execute_sql_command(connection, sql_command):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_command)
    except Error as e:
        print(e)

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
    sql_insert_campaign = ''' INSERT INTO campaigns(name,description,goal_amount,funded_amount,start_date,end_date)
                              VALUES(?,?,?,?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql_insert_campaign, campaign_data)
    connection.commit()
    return cursor.lastrowid

def modify_campaign_details(connection, updated_campaign_data):
    sql_update_campaign = ''' UPDATE campaigns
                              SET name = ?,
                                  description = ?,
                                  goal_amount = ?,
                                  funded_amount = ?,
                                  start_date = ?,
                                  end_date = ?
                              WHERE id = ?'''
    cursor = connection.cursor()
    cursor.execute(sql_update_campaign, updated_campaign_data)
    connection.commit()

def retrieve_all_campaigns(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM campaigns")

    campaign_rows = cursor.fetchall()

    for campaign in campaign_rows:
        print(campaign)

def retrieve_campaign_by_id(connection, campaign_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM campaigns WHERE id=?", (campaign_id,))

    campaign_details = cursor.fetchone()

    print(campaign_details)

if __name__ == '__main__':
    initialize_database()