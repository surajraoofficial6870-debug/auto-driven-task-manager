from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Database connection
def get_db():
    try:
        return mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=int(os.environ.get('DB_PORT', 3306))
        )
    except Error as e:
        print(f"DB Error: {e}")
        return None

# Initialize DB tables once
_initialized = False

def init_tables():
    global _initialized
    if _initialized:
        return
    _initialized = True
    
    conn = get_db()
    if not conn:
        print("Database not available at startup")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                status VARCHAR(50) DEFAULT 'pending'
            )
        """)
        conn.commit()
        print("Tables initialized")
    except Exception as e:
        print(f"Table init error: {e}")
    finally:
        cursor.close()
        conn.close()

# Health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    init_tables()
    return "🚀 Auto Driven Task Manager is Live on Railway with MySQL!"

@app.route("/signup", methods=["POST"])
def signup():
    init_tables()
    data = request.json
    conn = get_db()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (data["name"], data["email"], data["password"])
        )
        conn.commit()
        return jsonify({"msg": "User created"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    init_tables()
    conn = get_db()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return jsonify(tasks)
    finally:
        cursor.close()
        conn.close()

@app.route("/task", methods=["POST"])
def create_task():
    init_tables()
    data = request.json
    conn = get_db()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, status) VALUES (%s, %s)",
            (data["title"], data.get("status", "pending"))
        )
        conn.commit()
        return jsonify({"msg": "Task added"}), 201
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
