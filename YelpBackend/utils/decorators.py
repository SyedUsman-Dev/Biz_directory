from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from pymongo import MongoClient
from bson import ObjectId
from config import Config

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            client = MongoClient(Config.MONGO_URI)
            db = client.get_database()
            user = db.users.find_one({"_id": ObjectId(current_user_id)})
            
            if not user or user.get('role') != 'admin':
                return jsonify({"error": "Admin access required"}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        return decorator
    return wrapper
