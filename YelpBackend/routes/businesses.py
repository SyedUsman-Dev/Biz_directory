from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from config import Config
from utils.helpers import validate_object_id, serialize_doc, serialize_docs, error_response, success_response
from utils.decorators import admin_required

businesses_bp = Blueprint('businesses', __name__)

def get_db():
    client = MongoClient(Config.MONGO_URI)
    return client.get_database()

def update_business_rating(db, business_id):
    pipeline = [
        {"$match": {"businessId": business_id}},
        {"$group": {
            "_id": "$businessId",
            "averageRating": {"$avg": "$rating"},
            "count": {"$sum": 1}
        }}
    ]
    
    result = list(db.reviews.aggregate(pipeline))
    
    if result:
        db.businesses.update_one(
            {"_id": business_id},
            {
                "$set": {
                    "rating": round(result[0]['averageRating'], 1),
                    "reviewCount": result[0]['count']
                }
            }
        )
    else:
        db.businesses.update_one(
            {"_id": business_id},
            {"$set": {"rating": 0, "reviewCount": 0}}
        )

@businesses_bp.route('/', methods=['GET'])
def get_businesses():
    try:
        db = get_db()
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        rating_filter = request.args.get('rating')
        query = {}
        
        if rating_filter:
            try:
                min_rating = float(rating_filter)
                query['rating'] = {"$gte": min_rating}
            except ValueError:
                pass
        
        total = db.businesses.count_documents(query)
        businesses = list(db.businesses.find(query).skip(skip).limit(limit))
        
        return success_response({
            "businesses": serialize_docs(businesses),
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        })
    except Exception as e:
        return error_response(f"Failed to fetch businesses: {str(e)}", 500)

@businesses_bp.route('/search', methods=['GET'])
def search_businesses():
    try:
        db = get_db()
        
        name = request.args.get('name', '')
        city = request.args.get('city', '')
        state = request.args.get('state', '')
        category = request.args.get('category', '')
        rating_filter = request.args.get('rating')
        
        query = {}
        
        if name:
            query['name'] = {"$regex": name, "$options": "i"}
        if city:
            query['city'] = {"$regex": city, "$options": "i"}
        if state:
            query['state'] = {"$regex": state, "$options": "i"}
        if category:
            query['category'] = {"$regex": category, "$options": "i"}
        if rating_filter:
            try:
                min_rating = float(rating_filter)
                query['rating'] = {"$gte": min_rating}
            except ValueError:
                pass
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        total = db.businesses.count_documents(query)
        businesses = list(db.businesses.find(query).skip(skip).limit(limit))
        
        return success_response({
            "businesses": serialize_docs(businesses),
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        })
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)

@businesses_bp.route('/<business_id>', methods=['GET'])
def get_business(business_id):
    try:
        obj_id = validate_object_id(business_id)
        if not obj_id:
            return error_response("Invalid business ID", 400)
        
        db = get_db()
        business = db.businesses.find_one({"_id": obj_id})
        
        if not business:
            return error_response("Business not found", 404)
        
        return success_response({"business": serialize_doc(business)})
    except Exception as e:
        return error_response(f"Failed to fetch business: {str(e)}", 500)

@businesses_bp.route('/', methods=['POST'])
@jwt_required()
def create_business():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'city', 'state', 'address', 'category']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"{field} is required", 400)
        
        db = get_db()
        
        business = {
            "name": data['name'],
            "city": data['city'],
            "state": data['state'],
            "address": data['address'],
            "category": data['category'],
            "phone": data.get('phone', ''),
            "rating": 0,
            "reviewCount": 0,
            "createdAt": datetime.utcnow()
        }
        
        result = db.businesses.insert_one(business)
        business['_id'] = result.inserted_id
        
        return success_response({
            "message": "Business created successfully",
            "business": serialize_doc(business)
        }, 201)
    except Exception as e:
        return error_response(f"Failed to create business: {str(e)}", 500)

@businesses_bp.route('/<business_id>', methods=['PUT'])
@admin_required()
def update_business(business_id):
    try:
        obj_id = validate_object_id(business_id)
        if not obj_id:
            return error_response("Invalid business ID", 400)
        
        data = request.get_json()
        db = get_db()
        
        business = db.businesses.find_one({"_id": obj_id})
        if not business:
            return error_response("Business not found", 404)
        
        update_data = {}
        allowed_fields = ['name', 'city', 'state', 'address', 'category', 'phone']
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if update_data:
            db.businesses.update_one({"_id": obj_id}, {"$set": update_data})
        
        updated_business = db.businesses.find_one({"_id": obj_id})
        
        return success_response({
            "message": "Business updated successfully",
            "business": serialize_doc(updated_business)
        })
    except Exception as e:
        return error_response(f"Failed to update business: {str(e)}", 500)

@businesses_bp.route('/<business_id>', methods=['DELETE'])
@admin_required()
def delete_business(business_id):
    try:
        obj_id = validate_object_id(business_id)
        if not obj_id:
            return error_response("Invalid business ID", 400)
        
        db = get_db()
        
        business = db.businesses.find_one({"_id": obj_id})
        if not business:
            return error_response("Business not found", 404)
        
        db.reviews.delete_many({"businessId": obj_id})
        db.businesses.delete_one({"_id": obj_id})
        
        return success_response({"message": "Business and associated reviews deleted successfully"})
    except Exception as e:
        return error_response(f"Failed to delete business: {str(e)}", 500)
