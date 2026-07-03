from backend.app.routes.main import main_bp
from backend.app.routes.accommodation import accommodation_bp
from backend.app.routes.promotion import promotion_bp
from backend.app.routes.booking import booking_bp
from backend.app.routes.report import report_bp
from backend.app.routes.dispute import dispute_bp
from backend.app.routes.payment import payment_bp
from backend.app.routes.message import message_bp

__all__ = ["main_bp", "accommodation_bp", "promotion_bp", "booking_bp", "report_bp", "dispute_bp", "payment_bp", "message_bp"]

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(accommodation_bp)
    app.register_blueprint(promotion_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(dispute_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(message_bp)
