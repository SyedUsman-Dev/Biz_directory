# Biz Directory - Backend API Project

## Project Overview
This is a Flask-based RESTful API backend for a business directory and review system, similar to Yelp. The project is an assignment for COM661 Full Stack Strategies and Development.

**Purpose**: Provide a complete backend API for managing businesses and reviews with user authentication and role-based access control.

**Dataset**: Based on the Yelp Dataset Challenge, featuring business listings and user reviews.

## Recent Changes
- **October 28, 2025**: Initial project setup
  - Created complete Flask API structure with authentication, businesses, and reviews endpoints
  - Implemented JWT-based authentication with role-based access control
  - Set up MongoDB integration with three collections (users, businesses, reviews)
  - Added comprehensive CRUD operations for all entities
  - Implemented search and filtering capabilities
  - Created data seeder script with sample data
  - Added startup script for MongoDB and Flask
  - Configured workflow to run the API on port 5000

## Project Architecture

### Technology Stack
- **Backend Framework**: Python Flask 3.1.2
- **Database**: MongoDB (NoSQL)
- **Authentication**: Flask-JWT-Extended (JWT tokens)
- **Security**: Werkzeug (password hashing), Flask-CORS
- **Environment**: python-dotenv for configuration

### Database Collections
1. **users**: User accounts with authentication and role information
2. **businesses**: Business listings with location and category data
3. **reviews**: User reviews linked to businesses and users via ObjectId references

### Project Structure
```
/
├── app.py              - Main Flask application with route registration
├── config.py           - Configuration management
├── routes/             - API endpoint blueprints
│   ├── auth.py        - Authentication (register, login, /me)
│   ├── businesses.py  - Business CRUD and search
│   └── reviews.py     - Review CRUD with ownership checks
├── utils/              - Helper utilities
│   ├── decorators.py  - Custom decorators (admin_required, etc.)
│   └── helpers.py     - Serialization and validation helpers
├── start.sh           - Startup script (MongoDB + Flask)
├── seed_data.py       - Sample data generator
└── README.md          - Complete API documentation
```

### Key Features Implemented
- User registration and JWT login
- Role-based access (public, user, admin)
- Full CRUD for businesses (with admin-only edit/delete)
- Full CRUD for reviews (with ownership validation)
- Search by name, city, state, category, rating
- Pagination support
- Automatic business rating calculation from reviews
- Comprehensive error handling and validation
- RESTful design with proper HTTP status codes

## User Preferences
- Backend-only project (no frontend required)
- Focus on API functionality and RESTful design
- Emphasis on proper authentication and authorization
- Need for comprehensive Postman testing support

## Running the Project
```bash
bash start.sh
```

The API will be available at: http://localhost:5000

To seed sample data:
```bash
python seed_data.py
```

Test accounts after seeding:
- Admin: admin@bizdirectory.com / admin123
- User: john@example.com / password123

## Assignment Requirements Addressed
✅ Python Flask API
✅ MongoDB database integration
✅ Full CRUD operations (create, retrieve, update, delete)
✅ User authentication with JWT
✅ Role-based access control
✅ Search and filtering functionality
✅ Pagination support
✅ Input validation and error handling
✅ RESTful design with proper HTTP methods and status codes
✅ Code structure and organization
✅ Comprehensive documentation

## Next Steps for Student
1. Test all endpoints using Postman
2. Create Postman test collection with automated tests
3. Generate Postman API documentation
4. Export MongoDB collections using mongoexport
5. Record demonstration video (max 5 minutes)
6. Prepare submission package
