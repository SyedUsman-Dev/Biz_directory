#!/usr/bin/env python
import json
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

MONGO_URI = 'mongodb://localhost:27017/biz_directory'

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()
    
    return doc

def export_collection(db, collection_name, output_file):
    """Export a MongoDB collection to a JSON file"""
    print(f"Exporting {collection_name} collection...")
    
    collection = db[collection_name]
    documents = list(collection.find())
    
    serialized_docs = [serialize_doc(doc) for doc in documents]
    
    with open(output_file, 'w') as f:
        json.dump(serialized_docs, f, indent=2)
    
    print(f"✓ {len(serialized_docs)} documents exported to {output_file}")
    return len(serialized_docs)

def main():
    print("=" * 60)
    print("MongoDB Data Export for Assignment Submission")
    print("=" * 60)
    print()
    
    os.makedirs('exports', exist_ok=True)
    
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_database()
        
        total_users = export_collection(db, 'users', 'exports/users.json')
        total_businesses = export_collection(db, 'businesses', 'exports/businesses.json')
        total_reviews = export_collection(db, 'reviews', 'exports/reviews.json')
        
        print()
        print("=" * 60)
        print("Export Complete!")
        print("=" * 60)
        print(f"Users:      {total_users} documents")
        print(f"Businesses: {total_businesses} documents")
        print(f"Reviews:    {total_reviews} documents")
        print()
        print("All files saved in the 'exports' directory:")
        print("  - exports/users.json")
        print("  - exports/businesses.json")
        print("  - exports/reviews.json")
        print()
        print("To create submission ZIP:")
        print("  cd exports && zip ../biz-directory-mongodb.zip *.json")
        
    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Make sure MongoDB is running and the database exists.")
        print("Run 'python seed_data.py' to create sample data.")

if __name__ == "__main__":
    main()
