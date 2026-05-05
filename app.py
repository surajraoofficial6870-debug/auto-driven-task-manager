from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# DB connect function (better practice)
def get_db():
    conn = sqlite3.connect("task.db")
    conn.row_factory = sqlite3.Row
    return conn

# tables create (startup pe)
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "🚀 Task Manager Running"

# signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name,email,password) VALUES (?,?,?)",
        (data["name"], data["email"], data["password"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "User created"})

# create task
@app.route("/task", methods=["POST"])
def create_task():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title,status) VALUES (?,?)",
        (data["title"], "pending")
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "Task added"})

# get tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in tasks])

# ⚠️ IMPORTANT for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)