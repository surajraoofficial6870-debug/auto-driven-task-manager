from flask import request, jsonify
import jwt

def auth_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"msg": "Token missing"}), 401

        try:
            data = jwt.decode(token.split(" ")[1], "secret123", algorithms=["HS256"])
            request.user = data
        except:
            return jsonify({"msg": "Invalid token"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper