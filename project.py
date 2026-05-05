from flask import Blueprint, request, jsonify
from models import Project
from db import db
from middleware import auth_required

project_routes = Blueprint("projects", __name__)

@project_routes.route("/", methods=["POST"])
@auth_required
def create_project():
    if request.user["role"] != "admin":
        return jsonify({"msg": "Only admin can create project"}), 403

    data = request.json

    project = Project(
        name=data["name"],
        description=data.get("description"),
        created_by=request.user["id"]
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({"msg": "Project created"})


@project_routes.route("/", methods=["GET"])
@auth_required
def get_projects():
    projects = Project.query.all()

    result = []
    for p in projects:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description
        })

    return jsonify(result)