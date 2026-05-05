from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# DB create/connect
conn = sqlite3.connect("task.db", check_same_thread=False)
cursor = conn.cursor()

# tables
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

@app.route("/")
def home():
    return "🚀 Task Manager Running"

# signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    cursor.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                   (data["name"], data["email"], data["password"]))
    conn.commit()
    return jsonify({"msg": "User created"})

# create task
@app.route("/task", methods=["POST"])
def create_task():
    data = request.json
    cursor.execute("INSERT INTO tasks (title,status) VALUES (?,?)",
                   (data["title"], "pending"))
    conn.commit()
    return jsonify({"msg": "Task added"})

# get tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return jsonify(cursor.fetchall())

app.run(host="0.0.0.0", port=5000)