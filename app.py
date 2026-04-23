from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from db import init_db

# Import route blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.categories import categories_bp
from routes.orders import orders_bp
from routes.addresses import addresses_bp
from routes.shipping import shipping_bp
from routes.webhooks import webhooks_bp
from routes.admin_shipping import admin_shipping_bp
from routes.payment import payment_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(addresses_bp)
    app.register_blueprint(shipping_bp)
    app.register_blueprint(webhooks_bp)
    app.register_blueprint(admin_shipping_bp)
    app.register_blueprint(payment_bp)

    # Health check route
    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify(
            {
                "status": "success",
                "message": "Trollz Store API is running",
                "version": "1.0.0",
            }
        )

    # 404 handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Route not found"}), 404

    # 500 handler
    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({"status": "error", "message": "Internal server error"}),
            500,
        )

    return app


if __name__ == "__main__":
    # Initialize database tables
    print("[APP] Initializing database...")
    init_db()

    # Create and run app
    app = create_app()
    print(f"[APP] Starting Trollz Store API on {Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
