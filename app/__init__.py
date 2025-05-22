from flask import Flask, redirect, url_for
from app.extensions import db, migrate, login_manager
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    # Inisialisasi extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)  # tanpa prefix, biar handle root

    from app.routes.user import user
    app.register_blueprint(user, url_prefix='/user')

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Root route
    @app.route('/')
    def index():
        return redirect(url_for('auth.home'))

    with app.app_context():
        db.create_all()

    return app
