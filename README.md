# Inventory Management API

A RESTful Inventory Management API built with **Python, FastAPI, SQLAlchemy, and PostgreSQL**. This project provides backend functionality for managing products, tracking inventory quantities, and organizing product data through structured API endpoints.

Built as a practical backend development project to demonstrate REST API design, database integration, data validation, and automated testing.

## Features

- **Product Management (CRUD)**
  - Create new products.
  - Retrieve all products.
  - Retrieve individual products by ID.
  - Update product information using partial updates.
  - Delete products.
- **Search and Filtering**
  - Search products by name.
  - Filter products by category.
- **Pagination**
  - Control the number of returned products.
  - Navigate through product records using offset and limit.
- **Data Validation**
  - Validate incoming requests using Pydantic.
  - Handle invalid input and missing products.
- **Database Integration**
  - PostgreSQL database.
  - SQLAlchemy ORM.
  - Environment-based database configuration.
- **Automated Testing**
  - Pytest.
  - FastAPI TestClient.
  - SQLite-based test database.
  - Tests for CRUD operations, validation, filtering, and pagination.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Request validation and response schemas |
| Pytest | Automated testing |
| Git & GitHub | Version control |

## Project Structure

```text
inventory-management-api/
│
├── app/
│   ├── database/
│   │   ├── connection.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   └── __init__.py
│   │
│   ├── routers/
│   │   ├── products.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── product_service.py
│   │   └── __init__.py
│   │
│   └── main.py
│
├── tests/
│   └── test_products.py
│
├── .env
├── .gitignore
├── requirements.txt
└── test_connection.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sameerbist01/inventory-management-api.git
cd inventory-management-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```powershell
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Create a PostgreSQL database named:

```text
inventory_db
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/inventory_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products/` | Create a product |
| GET | `/products/` | Get all products |
| GET | `/products/{product_id}` | Get a product by ID |
| PATCH | `/products/{product_id}` | Partially update a product |
| DELETE | `/products/{product_id}` | Delete a product |

### Example: Create a Product

**POST** `/products/`

```json
{
  "name": "Coca Cola",
  "price": 1.5,
  "quantity": 100,
  "category": "Beverages"
}
```

### Example: Search and Filter

```text
GET /products/?name=coca&category=Beverages&skip=0&limit=10
```

## Running Tests

Run the automated test suite:

```bash
pytest -v
```

The tests cover product CRUD operations, invalid inputs, missing products, search, category filtering, and pagination.

## Development Roadmap

- [x] FastAPI project setup
- [x] Product CRUD operations
- [x] PostgreSQL integration
- [x] SQLAlchemy ORM
- [x] Search and filtering
- [x] Pagination
- [x] Pydantic validation
- [x] Automated API tests
- [ ] Alembic database migrations
- [ ] JWT authentication and authorization
- [ ] User roles and permissions
- [ ] Stock-in and stock-out management
- [ ] Inventory movement history
- [ ] Supplier management
- [ ] Low-stock alerts
- [ ] Sales and inventory reports
- [ ] Docker integration
- [ ] Deployment
- [ ] React frontend

## Project Status

**Currently under active development.**

The current version implements product management, PostgreSQL integration, search, filtering, pagination, and automated tests. Additional inventory management features are planned.

## Author

**Sameer Bist**

- GitHub: [@Sameerbist01](https://github.com/Sameerbist01)

---

If you find this project interesting, consider giving it a ⭐ on GitHub!
