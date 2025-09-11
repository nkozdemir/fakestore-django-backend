# FakeStore Django Backend

This project is a Django backend that mirrors the [FakeStore API](https://fakestoreapi.com/docs) using a local PostgreSQL database. It provides endpoints to fetch and manipulate products, carts, and users.

## Features
- Local PostgreSQL database storage for all data
- Complete API for products, carts, users, and authentication
- PostgreSQL database via Docker Compose
- Redis caching for improved performance
- Django 5.x, Python 3.13

## Setup

### 1. Clone the repository
```
git clone <repo-url>
cd fakestore-django-backend
```

### 2. Run the full stack with Docker (PostgreSQL + Redis + Django app)
```
docker compose up --build
```

This will start:
- PostgreSQL (service: db)
- Redis (service: redis)
- Django app (service: web at http://localhost:8000)

### 3. Create and activate a Python virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Set up the database (migrations, import data, create users)
```
# Start Docker services (PostgreSQL and Redis) and set up the database
python manage.py setup_db --with-docker
```

Or if you want to reset the database first:
```
python manage.py setup_db --force --with-docker
```

This command will:
1. Start Docker services (PostgreSQL and Redis)
2. Apply all migrations
3. Import all data from FakeStore API
4. Create Django users for all FakeStore users

### 6. Run the development server (non-Docker)
If you prefer running Django locally while still using Docker for Postgres/Redis:
```
docker compose up -d db redis
python manage.py runserver
```

## API Endpoints

### Products
- `GET /api/products/` — List all products 
- `POST /api/products/` — Create a new product
- `GET /api/products/<id>/` — Get product by ID
- `PUT /api/products/<id>/` — Update a product completely
- `PATCH /api/products/<id>/` — Update a product partially
- `DELETE /api/products/<id>/` — Delete a product

### Users
- `GET /api/users/` — List all users
- `POST /api/users/` — Create a new user
- `GET /api/users/<id>/` — Get user by ID
- `PUT /api/users/<id>/` — Update a user completely
- `DELETE /api/users/<id>/` — Delete a user

### Carts
- `GET /api/carts/` — List all carts
- `POST /api/carts/` — Create a new cart
- `GET /api/carts/<id>/` — Get cart by ID
- `PUT /api/carts/<id>/` — Update a cart completely
- `DELETE /api/carts/<id>/` — Delete a cart
- `GET /api/carts/user/<user_id>/` — Get carts by user ID

### Authentication
- `POST /api/auth/register/` — Register a new user (returns JWT tokens)
- `POST /api/auth/login/` — Login with username and password (returns JWT tokens)
- `POST /api/auth/refresh/` — Refresh an expired access token
- `GET /api/auth/me/` — Get information about the current user (requires authentication)
 - `POST /api/auth/logout/` — Logout by blacklisting a single refresh token (body: {"refresh": "<token>"})
 - `POST /api/auth/logout-all/` — Logout from all sessions (requires authentication)

## Environment Variables
- Database settings are configured in `fakestore_backend/settings.py` for local Docker PostgreSQL.

## JWT Authentication

This project uses Django REST Framework SimpleJWT for authentication. Here's how to use the JWT authentication endpoints:

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpassword123"}'
```

### Login with username and password
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword123"}'
```

The response will contain both access and refresh tokens:
```json
{
  "refresh": "eyJ0eXAiOiJKV...",
  "access": "eyJ0eXAiOiJKV...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### Refresh an expired token
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### Access protected endpoints
```bash
curl http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## License
MIT
