from flask import Flask
from app.extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdb.db'
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)  # Remove url_prefix to allow root route handling

    from app.routes.user import user
    app.register_blueprint(user, url_prefix='/user')  # opsional: kasih prefix untuk user

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # prefix opsional

    with app.app_context():
        db.create_all()  # Create database tables

    return app
