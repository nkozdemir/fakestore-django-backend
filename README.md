# FakeStore Django Backend

This project is a Django backend that acts as a proxy and wrapper for the [FakeStore API](https://fakestoreapi.com/docs). It provides endpoints to fetch products and categories, and is configured to use a PostgreSQL database running in Docker.

## Features
- Proxy endpoints for products and categories from FakeStore API
- PostgreSQL database via Docker Compose
- Django 5.x, Python 3.13

## Setup

### 1. Clone the repository
```
git clone <repo-url>
cd fakestore-django-backend
```

### 2. Start PostgreSQL with Docker Compose
```
docker compose up -d
```

### 3. Create and activate a Python virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Apply migrations
```
python manage.py migrate
```

### 6. Run the development server
```
python manage.py runserver
```

## API Endpoints
- `/api/products/` — List all products
- `/api/products/<id>/` — Get product by ID
- `/api/categories/` — List all categories
- `/api/categories/<category>/` — List products in a category

## Environment Variables
- Database settings are configured in `fakestore_backend/settings.py` for local Docker PostgreSQL.

## License
MIT
