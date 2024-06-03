from flask import Flask, request, jsonify
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route('/campaigns', methods=['POST'])
def add_campaign():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "INSERT INTO campaigns (name, target_amount, current_amount) VALUES (%s, %s, %s) RETURNING *;",
            (data['name'], data['target_amount'], 0))
        
        new_campaign = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(new_campaign), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/campaigns', methods=['GET'])
def list_campaigns():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT * FROM campaigns;")
    campaigns = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify(campaigns), 200

@app.route('/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute(
            "UPDATE campaigns SET current_amount = current_amount + %s WHERE id = %s RETURNING *;",
            (data['amount'], campaign asd')])
        
        updated_campaign = cur.fetchone()
        conn.commit()

        if updated_campaign is None:
            return jsonify({'message': 'Campaign not found'}), 404
        
        cur.close()
        conn.close()
        
        return jsonify(updated_campaign), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)