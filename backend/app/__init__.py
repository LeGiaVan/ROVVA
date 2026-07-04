import os

from flask import Flask

from backend.app.config import config_by_name
from backend.app.extensions import db, login_manager
from backend.app.routes import register_blueprints


def create_app(config_name="default"):
    config = config_by_name[config_name]
    os.makedirs(config.INSTANCE_DIR, exist_ok=True)

    app = Flask(
        __name__,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,
        static_url_path="/static",
        instance_path=config.INSTANCE_DIR,
    )
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    @login_manager.user_loader
    def load_user(user_id):
        from backend.app.models import User
        return User.query.get(int(user_id))

    register_blueprints(app)
    register_cli(app)

    with app.app_context():
        from backend.app import models  # noqa: F401

        db.create_all()
        from backend.app.seed import seed_database

        seed_database()

    return app


def register_cli(app):
    @app.cli.command("seed")
    def seed_command():
        """Reset and seed the database with sample data."""
        from backend.app.seed import seed_database

        db.drop_all()
        db.create_all()
        if seed_database():
            print("Database seeded successfully.")
        else:
            print("Database already contains data. Use drop/create first.")
