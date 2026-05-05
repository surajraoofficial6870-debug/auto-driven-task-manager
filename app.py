from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# --- STEP 2: MySQL Connection Logic ---
def get_db():
    try:
        # Ye variables Railway ke "Variables" tab (image_00969f.png) se matching hain
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=os.environ.get('DB_PORT')
        )
        return conn
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None

def init_db():
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        # MySQL Syntax: AUTO_INCREMENT (SQLite se thoda alag)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            status VARCHAR(50)
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Startup par table create karega
init_db()

@app.route("/")
def home():
    return "🚀 Auto Driven Task Manager is Live with MySQL!"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    
    cursor = conn.cursor()
    # MySQL mein %s use hota hai placeholder ke liye
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["password"])
    )
    conn.commit()
    conn.close()
    return jsonify({"msg": "User created"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True) # dictionary=True taaki JSON output sahi mile
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

# Railway ke liye port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)