from flask import Blueprint, request, jsonify
from models import User
from db import db
import bcrypt
import jwt

auth_routes = Blueprint("auth", __name__)

# signup
@auth_routes.route("/signup", methods=["POST"])
def signup():
    data = request.json

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed.decode(),
        role=data.get("role", "member")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"})

# login
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"msg": "User nahi mila"})

    if not bcrypt.checkpw(data["password"].encode(), user.password.encode()):
        return jsonify({"msg": "Wrong password"})

    token = jwt.encode({"id": user.id, "role": user.role}, "secret123", algorithm="HS256")

    return jsonify({"token": token})