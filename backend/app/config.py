import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-rova-host-secret")
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'rova_host.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
    TEMPLATE_FOLDER = os.path.join(FRONTEND_DIR, "templates")
    STATIC_FOLDER = os.path.join(FRONTEND_DIR, "static")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
