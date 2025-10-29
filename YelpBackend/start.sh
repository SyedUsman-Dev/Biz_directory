#!/bin/bash

mkdir -p data/db

echo "Starting MongoDB..."
mongod --dbpath data/db --bind_ip 127.0.0.1 --port 27017 --fork --logpath data/mongodb.log

echo "Waiting for MongoDB to start..."
sleep 3

echo "Starting Flask API..."
python app.py
