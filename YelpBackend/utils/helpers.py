from bson import ObjectId
from flask import jsonify

def validate_object_id(id_string):
    try:
        return ObjectId(id_string)
    except:
        return None

def serialize_doc(doc):
    if doc is None:
        return None
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    if 'userId' in doc:
        doc['userId'] = str(doc['userId'])
    if 'businessId' in doc:
        doc['businessId'] = str(doc['businessId'])
    return doc

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code

def success_response(data, status_code=200):
    return jsonify(data), status_code
