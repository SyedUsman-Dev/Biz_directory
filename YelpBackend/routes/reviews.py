from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from config import Config
from utils.helpers import validate_object_id, serialize_doc, serialize_docs, error_response, success_response
from utils.decorators import admin_required

reviews_bp = Blueprint('reviews', __name__)

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

@reviews_bp.route('/businesses/<business_id>/reviews', methods=['GET'])
def get_business_reviews(business_id):
    try:
        obj_id = validate_object_id(business_id)
        if not obj_id:
            return error_response("Invalid business ID", 400)
        
        db = get_db()
        
        business = db.businesses.find_one({"_id": obj_id})
        if not business:
            return error_response("Business not found", 404)
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        total = db.reviews.count_documents({"businessId": obj_id})
        reviews = list(db.reviews.find({"businessId": obj_id}).skip(skip).limit(limit).sort("createdAt", -1))
        
        for review in reviews:
            user = db.users.find_one({"_id": review['userId']})
            if user:
                review['username'] = user['username']
        
        return success_response({
            "reviews": serialize_docs(reviews),
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        })
    except Exception as e:
        return error_response(f"Failed to fetch reviews: {str(e)}", 500)

@reviews_bp.route('/businesses/<business_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(business_id):
    try:
        obj_id = validate_object_id(business_id)
        if not obj_id:
            return error_response("Invalid business ID", 400)
        
        data = request.get_json()
        
        if not data.get('rating') or not data.get('text'):
            return error_response("Rating and text are required", 400)
        
        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return error_response("Rating must be between 1 and 5", 400)
        except ValueError:
            return error_response("Rating must be a number", 400)
        
        current_user_id = get_jwt_identity()
        db = get_db()
        
        business = db.businesses.find_one({"_id": obj_id})
        if not business:
            return error_response("Business not found", 404)
        
        existing_review = db.reviews.find_one({
            "businessId": obj_id,
            "userId": ObjectId(current_user_id)
        })
        
        if existing_review:
            return error_response("You have already reviewed this business", 409)
        
        review = {
            "businessId": obj_id,
            "userId": ObjectId(current_user_id),
            "rating": rating,
            "text": data['text'],
            "createdAt": datetime.utcnow()
        }
        
        result = db.reviews.insert_one(review)
        review['_id'] = result.inserted_id
        
        update_business_rating(db, obj_id)
        
        user = db.users.find_one({"_id": ObjectId(current_user_id)})
        if user:
            review['username'] = user['username']
        
        return success_response({
            "message": "Review created successfully",
            "review": serialize_doc(review)
        }, 201)
    except Exception as e:
        return error_response(f"Failed to create review: {str(e)}", 500)

@reviews_bp.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    try:
        obj_id = validate_object_id(review_id)
        if not obj_id:
            return error_response("Invalid review ID", 400)
        
        db = get_db()
        review = db.reviews.find_one({"_id": obj_id})
        
        if not review:
            return error_response("Review not found", 404)
        
        user = db.users.find_one({"_id": review['userId']})
        if user:
            review['username'] = user['username']
        
        return success_response({"review": serialize_doc(review)})
    except Exception as e:
        return error_response(f"Failed to fetch review: {str(e)}", 500)

@reviews_bp.route('/reviews/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    try:
        obj_id = validate_object_id(review_id)
        if not obj_id:
            return error_response("Invalid review ID", 400)
        
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        db = get_db()
        review = db.reviews.find_one({"_id": obj_id})
        
        if not review:
            return error_response("Review not found", 404)
        
        user = db.users.find_one({"_id": ObjectId(current_user_id)})
        
        if not user:
            return error_response("User not found", 404)
        
        if str(review['userId']) != current_user_id and user.get('role') != 'admin':
            return error_response("You can only edit your own reviews", 403)
        
        update_data = {}
        
        if 'rating' in data:
            try:
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    return error_response("Rating must be between 1 and 5", 400)
                update_data['rating'] = rating
            except ValueError:
                return error_response("Rating must be a number", 400)
        
        if 'text' in data:
            update_data['text'] = data['text']
        
        if update_data:
            db.reviews.update_one({"_id": obj_id}, {"$set": update_data})
            
            if 'rating' in update_data:
                update_business_rating(db, review['businessId'])
        
        updated_review = db.reviews.find_one({"_id": obj_id})
        
        if updated_review:
            user = db.users.find_one({"_id": updated_review['userId']})
            if user:
                updated_review['username'] = user['username']
        
        return success_response({
            "message": "Review updated successfully",
            "review": serialize_doc(updated_review)
        })
    except Exception as e:
        return error_response(f"Failed to update review: {str(e)}", 500)

@reviews_bp.route('/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    try:
        obj_id = validate_object_id(review_id)
        if not obj_id:
            return error_response("Invalid review ID", 400)
        
        current_user_id = get_jwt_identity()
        db = get_db()
        
        review = db.reviews.find_one({"_id": obj_id})
        
        if not review:
            return error_response("Review not found", 404)
        
        user = db.users.find_one({"_id": ObjectId(current_user_id)})
        
        if not user:
            return error_response("User not found", 404)
        
        if str(review['userId']) != current_user_id and user.get('role') != 'admin':
            return error_response("You can only delete your own reviews or you must be an admin", 403)
        
        business_id = review['businessId']
        
        db.reviews.delete_one({"_id": obj_id})
        
        update_business_rating(db, business_id)
        
        return success_response({"message": "Review deleted successfully"})
    except Exception as e:
        return error_response(f"Failed to delete review: {str(e)}", 500)
