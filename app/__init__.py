<<<<<<< HEAD
from flask import Flask, redirect, url_for
from .extensions import db, migrate, login_manager
from app.models import User
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
=======
from flask import Flask
from app.extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdb.db'
    app.config['SECRET_KEY'] = 'your-secret-key'
>>>>>>> dbd657281f5a6ccc42ee16120d6febdfb2c7ee73

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)  # Remove url_prefix to allow root route handling

    from app.routes.user import user
    app.register_blueprint(user, url_prefix='/user')  # opsional: kasih prefix untuk user

<<<<<<< HEAD
    # Register blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Root route
    @app.route('/')
    def index():
        return redirect(url_for('auth.home'))
=======
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # prefix opsional
>>>>>>> dbd657281f5a6ccc42ee16120d6febdfb2c7ee73

    with app.app_context():
        db.create_all()  # Create database tables

    return app
