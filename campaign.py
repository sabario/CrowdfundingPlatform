import os
from datetime import datetime
import sqlite3
DB_PATH = os.getenv("CROWDFUNDING_DB_PATH", "crowdfunding_platform.db")
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
    except Exception as e:
        print(e)
    return conn
def create_campaign(campaign_details):
    conn = create_connection()
    sql = ''' INSERT INTO campaigns(name,target_amount,start_date,end_date)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, campaign_details)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
def get_campaigns():
    conn = create_connection()
    sql = "SELECT * FROM campaigns"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        campaigns = cur.fetchall()
        return campaigns
    except Exception as e:
        print(e)
        return []
    finally:
        if conn:
            conn.close()
def make_contribution(campaign_id, amount):
    conn = create_connection()
    sql = ''' INSERT INTO contributions(campaign_id,amount,contribution_date)
              VALUES(?,?,?) '''
    contribution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cur = conn.cursor()
        cur.execute(sql, (campaign_id, amount, contribution_date))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
if __name__ == "__main__":
    create_campaign(("Save The Whales", 5000, "2023-01-01", "2023-12-31"))
    make_contribution(1, 50)
    all_campaigns = get_campaigns()
    print(all_campaigns)