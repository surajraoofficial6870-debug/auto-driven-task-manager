from flask import Blueprint, request, jsonify
from models import Task
from db import db
from middleware import auth_required

task_routes = Blueprint("tasks", __name__)

@task_routes.route("/", methods=["POST"])
@auth_required
def create_task():
    if request.user["role"] != "admin":
        return jsonify({"msg": "Only admin can assign tasks"}), 403

    data = request.json

    task = Task(
        title=data["title"],
        project_id=data["project_id"],
        assigned_to=data["assigned_to"],
        status="todo"
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"msg": "Task created"})


@task_routes.route("/", methods=["GET"])
@auth_required
def get_tasks():
    tasks = Task.query.all()

    result = []
    for t in tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "status": t.status
        })

    return jsonify(result)


@task_routes.route("/<int:id>", methods=["PUT"])
@auth_required
def update_task(id):
    data = request.json

    task = Task.query.get(id)
        

    db.session.commit()

    return jsonify({"msg": "Task updated"})