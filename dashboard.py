from flask import Blueprint, jsonify
from models import Task
from middleware import auth_required

dashboard_routes = Blueprint("dashboard", __name__)

@dashboard_routes.route("/", methods=["GET"])
@auth_required
def dashboard():
    tasks = Task.query.all()

    total = len(tasks)
    completed = len([t for t in tasks if t.status == "done"])
    pending = len([t for t in tasks if t.status != "done"])

    return jsonify({
        "total": total,
        "completed": completed,
        "pending": pending
    })