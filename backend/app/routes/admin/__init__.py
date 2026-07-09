from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

from backend.app.routes.admin import routes
