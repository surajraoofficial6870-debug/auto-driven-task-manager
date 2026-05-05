import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from db import db

# Blueprint imports
from auth import auth_routes
from project import project_routes
from task import task_routes
from dashboard import dashboard_routes

def create_app():
    # Frontend folder ka sahi path (kyunki tera frontend Backend ke andar hai)
    app = Flask(__name__, static_folder='frontend', static_url_path='/')

    # 1. CORS Configuration: Sab domains allow karne ke liye
    CORS(app)

    # 2. Database Configuration
    database_url = os.getenv('DATABASE_URL', 'sqlite:///task.db')
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'auto-driven-secret-key-6870')

    db.init_app(app)

    # 3. Register Blueprints
    app.register_blueprint(auth_routes, url_prefix="/api/auth")
    app.register_blueprint(project_routes, url_prefix="/api/projects")
    app.register_blueprint(task_routes, url_prefix="/api/tasks")
    app.register_blueprint(dashboard_routes, url_prefix="/api/dashboard")

    # 4. Serving Frontend from Flask (Optional but recommended for Railway)
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route("/health")
    def health():
        return jsonify({"status": "online", "message": "API is working fine"})

    # 5. Create Tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)