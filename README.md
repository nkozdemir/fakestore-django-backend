# FakeStore Django Backend

This project is a Django backend that mirrors the [FakeStore API](https://fakestoreapi.com/docs) using a local PostgreSQL database. It provides endpoints to fetch and manipulate products, carts, and users.

## Features
- Local PostgreSQL database storage for all data
- Complete API for products, carts, users, and authentication
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

### 6. Import all data from FakeStore API to the database
```
python manage.py import_all
```

### 7. Run the development server
```
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
- `POST /api/auth/login/` — Login with username and password (proxied directly to FakeStore API)

## Environment Variables
- Database settings are configured in `fakestore_backend/settings.py` for local Docker PostgreSQL.

## License
MIT
