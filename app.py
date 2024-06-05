from flask import Flask, request, jsonify
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except psycopg2.Error as e:
        # Could log or handle the specific database error here
        return None

@app.route('/campaigns', methods=['POST'])
def add_campaign():
    data = request.json
    if not data or 'name' not in data or 'target_amount' not in data:  # basic validation
        return jsonify({'error': 'Bad Request', 'message': 'Missing name or target_amount'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(error="Database connection failed"), 500

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "INSERT INTO campaigns (name, target_amount, current_amount) VALUES (%s, %s, %s) RETURNING *;",
            (data['name'], data['target_amount'], 0))
        new_campaign = cur.fetchone()
        conn.commit()
    except psycopg2.Error as e:
        return jsonify(error=f"Database query failed: {str(e)}"), 500
    finally:
        if conn:
            cur.close()
            conn.close()

    return jsonify(dict(new_campaign)), 201

@app.route('/campaigns', methods=['GET'])
def list_campaigns():
    conn = get_db_connection()
    if not conn:
        return jsonify(error="Database connection failed"), 500

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM campaigns;")
        campaigns = cur.fetchall()
    except psycopg2.Error as e:
        return jsonify(error=f"Failed to fetch campaigns: {str(e)}"), 500
    finally:
        if conn:
            cur.close()
            conn.close()

    return jsonify([dict(campaign) for campaign in campaigns]), 200

@app.route('/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    data = request.json
    if not data or 'amount' not in data:  # basic validation
        return jsonify({'error': 'Bad Request', 'message': 'Missing amount'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify(error="Database connection failed"), 500

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "UPDATE campaigns SET current_amount = current_amount + %s WHERE id = %s RETURNING *;",
            (data['amount'], campaign_id))
        updated_campaign = cur.fetchone()
        conn.commit()
        if updated_campaign is None:
            return jsonify({'message': 'Campaign not found'}), 404
    except psycopg2.Error as e:
        return jsonify(error=f"Failed to update campaign: {str(e)}"), 500
    finally:
        if conn:
            cur.close()
            conn.close()

    return jsonify(dict(updated_campaign)), 200

if __name__ == '__main__':
    app.run(debug=True)