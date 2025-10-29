#!/bin/bash

echo "========================================="
echo "Biz Directory API - Quick Test Suite"
echo "========================================="
echo ""

BASE_URL="http://localhost:5000"

echo "1. Testing API Root..."
curl -s $BASE_URL | python -m json.tool > /dev/null && echo "   ✓ API is responding" || echo "   ✗ API not responding"
echo ""

echo "2. Testing User Registration..."
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"quicktest","email":"quicktest@test.com","password":"test123"}')
echo "$REGISTER_RESPONSE" | grep -q "User registered successfully" && echo "   ✓ Registration working" || echo "   ✗ Registration failed"
echo ""

echo "3. Testing Admin Login..."
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bizdirectory.com","password":"admin123"}')
ADMIN_TOKEN=$(echo $ADMIN_LOGIN | python -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
if [ ! -z "$ADMIN_TOKEN" ]; then
  echo "   ✓ Admin login successful"
else
  echo "   ✗ Admin login failed"
fi
echo ""

echo "4. Testing Get All Businesses..."
BUSINESSES=$(curl -s $BASE_URL/api/businesses)
echo "$BUSINESSES" | grep -q "businesses" && echo "   ✓ Get businesses working" || echo "   ✗ Get businesses failed"
echo ""

echo "5. Testing Business Search..."
SEARCH=$(curl -s "$BASE_URL/api/businesses/search?city=New%20York")
echo "$SEARCH" | grep -q "businesses" && echo "   ✓ Search working" || echo "   ✗ Search failed"
echo ""

if [ ! -z "$ADMIN_TOKEN" ]; then
  echo "6. Testing Protected Endpoint (Admin)..."
  AUTH_TEST=$(curl -s $BASE_URL/api/auth/me -H "Authorization: Bearer $ADMIN_TOKEN")
  echo "$AUTH_TEST" | grep -q "admin" && echo "   ✓ Authentication working" || echo "   ✗ Authentication failed"
  echo ""
fi

echo "========================================="
echo "Test Suite Complete!"
echo "========================================="
