from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson import ObjectId

MONGO_URI = 'mongodb://localhost:27017/biz_directory'

client = MongoClient(MONGO_URI)
db = client.get_database()

print("Clearing existing data...")
db.users.delete_many({})
db.businesses.delete_many({})
db.reviews.delete_many({})

print("Creating admin user...")
admin_user = {
    "username": "admin",
    "email": "admin@bizdirectory.com",
    "password": generate_password_hash("admin123"),
    "role": "admin",
    "createdAt": datetime.utcnow()
}
admin_id = db.users.insert_one(admin_user).inserted_id
print(f"Admin user created: admin@bizdirectory.com / admin123")

print("Creating regular user...")
user = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": generate_password_hash("password123"),
    "role": "user",
    "createdAt": datetime.utcnow()
}
user_id = db.users.insert_one(user).inserted_id
print(f"Regular user created: john@example.com / password123")

print("Creating sample businesses...")
businesses = [
    {
        "name": "Joe's Coffee Shop",
        "city": "New York",
        "state": "NY",
        "address": "123 Broadway Ave",
        "category": "Coffee & Tea",
        "phone": "212-555-0100",
        "rating": 0,
        "reviewCount": 0,
        "createdAt": datetime.utcnow()
    },
    {
        "name": "Pizza Palace",
        "city": "Brooklyn",
        "state": "NY",
        "address": "456 5th Street",
        "category": "Italian Restaurant",
        "phone": "718-555-0200",
        "rating": 0,
        "reviewCount": 0,
        "createdAt": datetime.utcnow()
    },
    {
        "name": "Tech Repair Shop",
        "city": "Manhattan",
        "state": "NY",
        "address": "789 Tech Ave",
        "category": "Electronics Repair",
        "phone": "212-555-0300",
        "rating": 0,
        "reviewCount": 0,
        "createdAt": datetime.utcnow()
    },
    {
        "name": "Green Garden Restaurant",
        "city": "Los Angeles",
        "state": "CA",
        "address": "321 Sunset Blvd",
        "category": "Vegan Restaurant",
        "phone": "310-555-0400",
        "rating": 0,
        "reviewCount": 0,
        "createdAt": datetime.utcnow()
    },
    {
        "name": "Book Haven",
        "city": "San Francisco",
        "state": "CA",
        "address": "654 Market Street",
        "category": "Bookstore",
        "phone": "415-555-0500",
        "rating": 0,
        "reviewCount": 0,
        "createdAt": datetime.utcnow()
    }
]

business_ids = []
for business in businesses:
    result = db.businesses.insert_one(business)
    business_ids.append(result.inserted_id)
    print(f"Created business: {business['name']}")

print("Creating sample reviews...")
reviews = [
    {
        "businessId": business_ids[0],
        "userId": user_id,
        "rating": 5,
        "text": "Amazing coffee! Best in the city. The baristas are friendly and the atmosphere is cozy.",
        "createdAt": datetime.utcnow()
    },
    {
        "businessId": business_ids[0],
        "userId": admin_id,
        "rating": 4,
        "text": "Great coffee, but sometimes the wait can be long during morning rush.",
        "createdAt": datetime.utcnow()
    },
    {
        "businessId": business_ids[1],
        "userId": user_id,
        "rating": 5,
        "text": "Authentic Italian pizza! The margherita is to die for.",
        "createdAt": datetime.utcnow()
    },
    {
        "businessId": business_ids[2],
        "userId": admin_id,
        "rating": 4,
        "text": "Fixed my phone quickly and at a reasonable price. Highly recommend!",
        "createdAt": datetime.utcnow()
    },
    {
        "businessId": business_ids[3],
        "userId": user_id,
        "rating": 5,
        "text": "Best vegan food in LA! The quinoa bowl is incredible.",
        "createdAt": datetime.utcnow()
    }
]

for review in reviews:
    db.reviews.insert_one(review)
    print(f"Created review for business ID: {review['businessId']}")

print("\nUpdating business ratings...")
for business_id in business_ids:
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

print("\nSeed data created successfully!")
print("\nTest Accounts:")
print("  Admin: admin@bizdirectory.com / admin123")
print("  User:  john@example.com / password123")
print(f"\nTotal Businesses: {len(businesses)}")
print(f"Total Reviews: {len(reviews)}")
