from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from config import Config
from utils.helpers import serialize_doc, error_response, success_response

auth_bp = Blueprint('auth', __name__)

def get_db():
    client = MongoClient(Config.MONGO_URI)
    return client.get_database()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return error_response("Username, email, and password are required", 400)
        
        db = get_db()
        
        if db.users.find_one({"email": data['email']}):
            return error_response("Email already exists", 409)
        
        if db.users.find_one({"username": data['username']}):
            return error_response("Username already exists", 409)
        
        user = {
            "username": data['username'],
            "email": data['email'],
            "password": generate_password_hash(data['password']),
            "role": "user",
            "createdAt": datetime.utcnow()
        }
        
        result = db.users.insert_one(user)
        user['_id'] = result.inserted_id
        
        return success_response({
            "message": "User registered successfully",
            "user": {
                "id": str(user['_id']),
                "username": user['username'],
                "email": user['email'],
                "role": user['role']
            }
        }, 201)
    except Exception as e:
        return error_response(f"Registration failed: {str(e)}", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return error_response("Email and password are required", 400)
        
        db = get_db()
        user = db.users.find_one({"email": data['email']})
        
        if not user or not check_password_hash(user['password'], data['password']):
            return error_response("Invalid email or password", 401)
        
        access_token = create_access_token(identity=str(user['_id']))
        
        return success_response({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": str(user['_id']),
                "username": user['username'],
                "email": user['email'],
                "role": user['role']
            }
        })
    except Exception as e:
        return error_response(f"Login failed: {str(e)}", 500)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        user = db.users.find_one({"_id": ObjectId(current_user_id)})
        
        if not user:
            return error_response("User not found", 404)
        
        return success_response({
            "user": {
                "id": str(user['_id']),
                "username": user['username'],
                "email": user['email'],
                "role": user['role']
            }
        })
    except Exception as e:
        return error_response(f"Failed to get user: {str(e)}", 500)
