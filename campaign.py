import os
from datetime import datetime
import sqlite3

DB_PATH = os.getenv("CROWDFUNDING_DB_PATH", "crowdfunding_platform.db")

conn = None

def create_connection():
    global conn
    if not conn:
        try:
            conn = sqlite3.connect(DB_PATH)
            print("Opened database successfully")
        except Exception as e:
            print(f"Database connection error: {e}")
    return conn

def close_connection():
    global conn
    if conn:
        conn.close()
        conn = None
        print("Closed database successfully")

def create_campaign(campaign_details):
    conn = create_connection()
    sql = ''' INSERT INTO campaigns(name, target_amount, start_date, end_date)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, campaign_details)
        conn.commit()
    except Exception as e:
        print(f"Error creating campaign: {e}")

def get_campaigns():
    conn = create_connection()
    sql = "SELECT * FROM campaigns"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        campaigns = cur.fetchall()
        return campaigns
    except Exception as e:
        print(f"Error retrieving campaigns: {e}")
        return []
        
def make_contribution(campaign_id, amount):
    conn = create_connection()
    sql = ''' INSERT INTO contributions(campaign_id, amount, contribution_date)
              VALUES(?,?,?) '''
    contribution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cur = conn.cursor()
        cur.execute(sql, (campaign_id, amount, contribution_date))
        conn.commit()
    except Exception as e:
        print(f"Error making contribution: {e}")

if __name__ == "__main__":
    try:
        create_campaign(("Save The Whales", 5000, "2023-01-01", "2023-12-31"))
        make_contribution(1, 50)
        all_campaigns = get_campaigns()
        print(all_campaigns)
    finally:
        close_connection()