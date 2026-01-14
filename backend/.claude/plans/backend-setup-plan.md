# Backend Setup Plan

## Overview
FastAPI backend for a pizzeria blog/tracking app focused on Berlin pizzerias with Google Maps integration.

---

## Database Recommendation: PostgreSQL

**Why PostgreSQL:**
- Excellent support for geographic data via PostGIS extension (useful for Google Maps integration)
- Strong JSON support for flexible data storage
- Mature, reliable, and well-documented
- Great performance for read-heavy workloads (blog-style app)
- Free and open source

**Alternative: SQLite**
- Good for development and small-scale deployments
- No separate server needed
- Easy to get started

---

## ORM Recommendation: SQLAlchemy with SQLModel

**Why SQLModel:**
- Built by the creator of FastAPI (Sebastián Ramírez)
- Combines SQLAlchemy and Pydantic models into one
- Reduces code duplication (one model for both database and API)
- Full async support with `asyncpg`
- Type hints and IDE autocompletion

**Dependencies to add:**
```
sqlmodel>=0.0.14
asyncpg>=0.29.0        # For async PostgreSQL
psycopg2-binary>=2.9.9 # For sync PostgreSQL (optional)
alembic>=1.13.0        # Database migrations
```

---

## Implementation Steps

### Phase 1: Database Setup
1. Install PostgreSQL locally or use Docker
2. Add SQLModel and database dependencies to requirements.txt
3. Create database configuration (connection string, settings)
4. Set up SQLModel engine and session management

### Phase 2: Models
1. Convert Pydantic models to SQLModel models
2. Add database fields (created_at, updated_at)
3. Create Pizzeria table with fields:
   - id (primary key)
   - name
   - address
   - latitude/longitude (for maps)
   - google_place_id (for Google Maps API)
   - rating
   - notes/review
   - visited_at
   - created_at
   - updated_at

### Phase 3: Database Migrations
1. Set up Alembic for migrations
2. Create initial migration
3. Add migration scripts to version control

### Phase 4: CRUD Operations
1. Create repository/service layer for database operations
2. Update endpoints to use database instead of in-memory storage
3. Add endpoints:
   - GET /pizzerias - List all
   - GET /pizzerias/{id} - Get one
   - POST /pizzerias - Create new
   - PUT /pizzerias/{id} - Update
   - DELETE /pizzerias/{id} - Delete

### Phase 5: Google Maps Integration
1. Set up Google Maps API credentials
2. Create service for Google Places API
3. Add endpoint to search/import pizzerias from Google Maps
4. Store Google place_id for linking

---

## Project Structure (Target)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py          # Settings and configuration
│   ├── database.py        # Database connection setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── pizzeria.py    # SQLModel models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── pizzerias.py   # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pizzeria.py    # Business logic
│   │   └── google_maps.py # Google Maps API integration
│   └── schemas/
│       └── pizzeria.py    # Request/Response schemas
├── alembic/               # Database migrations
├── tests/
├── plans/
├── .env                   # Environment variables (not committed)
├── .gitignore
├── alembic.ini
└── requirements.txt
```

---

## Environment Variables Needed

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_pizza
GOOGLE_MAPS_API_KEY=your_api_key_here
```

---

## Docker Setup (Optional)

```yaml
# docker-compose.yml for local PostgreSQL
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: pizza
      POSTGRES_PASSWORD: pizza
      POSTGRES_DB: ai_pizza
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```
