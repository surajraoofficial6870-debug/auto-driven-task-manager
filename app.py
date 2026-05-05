from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# --- Database Connection ---
def get_db():
    try:
        # Railway ke environment variables use kar raha hai
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            port=os.environ.get('DB_PORT', 3306)
        )
        return conn
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# --- Initialize Tables ---
def init_db():
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Users Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
            """)
            # Tasks Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                status VARCHAR(50) DEFAULT 'pending'
            )
            """)
            conn.commit()
            print("✅ Tables initialized successfully!")
        except Error as e:
            print(f"❌ Table Creation Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Start up table creation
init_db()

@app.route("/")
def home():
    return "🚀 Auto Driven Task Manager is Live on Railway with MySQL!"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (data["name"], data["email"], data["password"])
        )
        conn.commit()
        return jsonify({"msg": "User created successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return jsonify(tasks)
    finally:
        conn.close()

@app.route("/task", methods=["POST"])
def create_task():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, status) VALUES (%s, %s)",
            (data["title"], data.get("status", "pending"))
        )
        conn.commit()
        return jsonify({"msg": "Task added"}), 201
    finally:
        conn.close()

if __name__ == "__main__":
    # Railway automatically assigns a port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)