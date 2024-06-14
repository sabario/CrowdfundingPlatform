import os
import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established: SQLite version", sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = DATABASE_URL

    sql_create_campaigns_table = """ CREATE TABLE IF NOT EXISTS campaigns (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text,
                                        target_amount real NOT NULL,
                                        current_amount real NOT NULL,
                                        start_date text,
                                        end_date text
                                    ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_campaigns_table)
    else:
        print("Error! cannot create the database connection.")

def add_campaign(conn, campaign):
    sql = ''' INSERT INTO campaigns(name,description,target_amount,current_amount,start_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, campaign)
    conn.commit()
    return cur.lastrowid

def update_campaign(conn, campaign):
    sql = ''' UPDATE campaigns
              SET name = ? ,
                  description = ? ,
                  target_amount = ?,
                  target_amount = ?,
                  start_date = ?,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, campaign)
    conn.commit()

def select_all_campaigns(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM campaigns")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_campaign_by_id(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM campaigns WHERE id=?", (id,))

    row = cur.fetchone()

    print(row)

if __name__ == '__main__':
    main()