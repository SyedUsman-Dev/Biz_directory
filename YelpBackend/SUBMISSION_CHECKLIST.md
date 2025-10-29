# COM661 Assignment Submission Checklist

## Required Submission Elements

### ✅ 1. Source Code (ZIP file)
**Status**: Ready to submit

**What to include**:
- [ ] app.py
- [ ] config.py
- [ ] routes/ directory (auth.py, businesses.py, reviews.py)
- [ ] utils/ directory (decorators.py, helpers.py)
- [ ] start.sh
- [ ] seed_data.py
- [ ] README.md
- [ ] .gitignore
- [ ] pyproject.toml (or requirements.txt)

**How to create**:
```bash
# From the project root
zip -r biz-directory-source.zip \
  app.py config.py routes/ utils/ \
  start.sh seed_data.py README.md \
  .gitignore pyproject.toml \
  -x "*.pyc" -x "__pycache__/*" -x "data/*"
```

### ✅ 2. MongoDB Collections (ZIP file)
**Status**: Export script ready

**What to include**:
- [ ] users.json
- [ ] businesses.json
- [ ] reviews.json

**How to create**:
```bash
# Run the export script
bash export_data.sh

# Create ZIP from exports
cd exports && zip ../biz-directory-mongodb.zip *.json && cd ..
```

### ⏳ 3. Video Demonstration (MAX 5 minutes)
**Status**: Script needed

**What to show**:
1. **Introduction (30 seconds)**
   - Brief overview of Biz Directory
   - Mention Yelp dataset
   - Explain purpose

2. **API Demonstration with Postman (3 minutes)**
   - Show user registration
   - Login (get JWT token)
   - Create a business
   - Add a review
   - Search businesses
   - Show admin operations (update/delete)
   - Demonstrate role-based access

3. **Code Walkthrough (1.5 minutes)**
   - Show project structure
   - Explain authentication system
   - Highlight key features (search, rating calculation)
   - Show database relationships

**Tips**:
- Practice to stay under 5 minutes
- Use Postman for clean API demos
- Keep code walkthrough high-level
- Show, don't tell

### ⏳ 4. PDF Documents

#### a) Complete Code Listing
**Status**: Code ready, needs PDF conversion

**How to create**:
```bash
# Option 1: Use an IDE to print to PDF
# Option 2: Use enscript + ps2pdf (Linux)
# Option 3: Copy code to Word/Google Docs and export as PDF
```

#### b) API Endpoints Summary
**Status**: Documented in README.md

**What to include**:
- List of all endpoints
- HTTP methods
- Required parameters
- Authentication requirements
- Example requests/responses

**Source**: See README.md sections:
- Authentication Endpoints
- Business Endpoints
- Review Endpoints

#### c) Postman Test Results
**Status**: Need to run tests and capture results

**Steps**:
1. Import `postman_collection.json` into Postman
2. Create environment with `base_url` and `token`
3. Run seed script: `python seed_data.py`
4. Execute all requests
5. Create automated tests
6. Run collection with test runner
7. Export results as PDF

#### d) Postman API Documentation
**Status**: Collection created, needs documentation generation

**Steps**:
1. Import `postman_collection.json`
2. Add descriptions to each request
3. Add example responses
4. Use Postman's documentation feature
5. Export/publish documentation
6. Save as PDF

### ⏳ 5. Self-Evaluation Sheet
**Status**: Pending

**What to evaluate**:
- Database structure (15%)
- Database functionality (25%)
- API structure (25%)
- Usability (25%)
- Submission package (10%)

## Pre-Submission Tests

### Manual Testing Checklist
- [ ] Start fresh MongoDB instance
- [ ] Run seed script
- [ ] Test all authentication endpoints
- [ ] Test all business CRUD operations
- [ ] Test all review CRUD operations
- [ ] Verify search functionality
- [ ] Verify pagination
- [ ] Test role-based access control
- [ ] Verify error handling

### Quick Test Command
```bash
bash test_api.sh
```

## Submission Timeline

**Current Date**: October 28, 2025
**Deadline**: Monday, November 3, 2025 at 12:00 PM (Noon)

**Recommended Schedule**:
- **Oct 28**: ✅ Complete backend development
- **Oct 29**: Test with Postman, create test collection
- **Oct 30**: Generate documentation, prepare PDFs
- **Oct 31**: Record and edit video
- **Nov 1**: Review all materials, create ZIPs
- **Nov 2**: Final review, ensure completeness
- **Nov 3**: Submit before noon

## Quality Checks

### Code Quality
- [x] Proper error handling
- [x] Input validation
- [x] Security measures (JWT, password hashing)
- [x] Code organization and structure
- [x] Comments where needed
- [x] No hardcoded secrets

### Documentation Quality
- [x] Clear README with setup instructions
- [x] All endpoints documented
- [x] Example requests/responses
- [x] Database schema explained

### Functionality
- [x] Full CRUD on all collections
- [x] User authentication working
- [x] Role-based access control
- [x] Search and filtering
- [x] Pagination
- [x] Proper HTTP status codes

## Helpful Commands

### Start the API
```bash
bash start.sh
```

### Seed Sample Data
```bash
python seed_data.py
```

### Export MongoDB Data
```bash
bash export_data.sh
```

### Quick API Test
```bash
bash test_api.sh
```

### Check API Status
```bash
curl http://localhost:5000/health
```

## Submission URLs/Locations
- **Blackboard**: CW1 Submission link in Assessment area
- **Video**: Upload to required platform (check Blackboard)

## Notes
- Video over 5 min + 50% = max mark of 40%
- Source code and video are COMPULSORY
- Without either, submission is incomplete and cannot be marked
