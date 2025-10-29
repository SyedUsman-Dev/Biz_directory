from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.businesses import businesses_bp
from routes.reviews import reviews_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(businesses_bp, url_prefix='/api/businesses')
app.register_blueprint(reviews_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "message": "Biz Directory API",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "POST /api/auth/register": "Register a new user",
                "POST /api/auth/login": "Login and get JWT token",
                "GET /api/auth/me": "Get current user info (requires auth)"
            },
            "businesses": {
                "GET /api/businesses": "Get all businesses (with pagination)",
                "GET /api/businesses/search": "Search businesses by name, city, state, or category",
                "GET /api/businesses/<id>": "Get a single business by ID",
                "POST /api/businesses": "Create a new business (requires auth)",
                "PUT /api/businesses/<id>": "Update a business (admin only)",
                "DELETE /api/businesses/<id>": "Delete a business (admin only)"
            },
            "reviews": {
                "GET /api/businesses/<id>/reviews": "Get all reviews for a business",
                "POST /api/businesses/<id>/reviews": "Create a review (requires auth)",
                "GET /api/reviews/<id>": "Get a single review by ID",
                "PUT /api/reviews/<id>": "Update a review (owner or admin)",
                "DELETE /api/reviews/<id>": "Delete a review (owner or admin)"
            }
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
