from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

load_dotenv()

app = Flask(__name__)

# --- Database Connection ---
def get_db():
    try:
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_NAME')

        if host and host.startswith('mysql://'):
            parsed = urlparse(host)
            host = parsed.hostname
            if parsed.port:
                port = parsed.port
            if parsed.username and not user:
                user = parsed.username
            if parsed.password and not password:
                password = parsed.password
            if parsed.path and parsed.path != '/':
                database = parsed.path.lstrip('/')

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port) if port else 3306
        )
        return conn
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# --- Initialize Tables ---
def init_db():
    try:
        conn = get_db()
        if not conn:
            print("⚠️ Database unavailable at startup — skipping table initialization.")
            return
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
    except Exception as e:
        print(f"⚠️ Database initialization failed — app will continue without DB: {e}")

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
