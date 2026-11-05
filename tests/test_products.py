
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.connection import Base, get_db


# Create a separate temporary SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Create a database session for each test request
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    # Save the original dependency overrides
    original_overrides = app.dependency_overrides.copy()

    # Use the temporary SQLite database
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        # Restore the original dependency overrides
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)

        # Remove temporary test tables
        Base.metadata.drop_all(bind=test_engine)

# First automated test
def test_create_product(client):
    response = client.post(
        "/products/",
        json={
            "name": "Test Keyboard",
            "price": 2500,
            "quantity": 10,
            "category": "Electronics"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Keyboard"
    assert data["price"] == 2500
    assert data["quantity"] == 10

def test_get_products(client):
    # Create a product first
    client.post(
        "/products/",
        json={
            "name": "Test Mouse",
            "price": 1500,
            "quantity": 5,
            "category": "Electronics"
        }
    )

    # Request all products
    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Test Mouse"

def test_get_product_by_id(client):
    # Create a product
    create_response = client.post(
        "/products/",
        json={
            "name": "Gaming Keyboard",
            "price": 3500,
            "quantity": 8,
            "category": "Electronics"
        }
    )

    product_id = create_response.json()["id"]

    # Retrieve the created product
    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Gaming Keyboard"

def test_update_product(client):
    # Create a product
    create_response = client.post(
        "/products/",
        json={
            "name": "Gaming Mouse",
            "price": 2000,
            "quantity": 10,
            "category": "Electronics"
        }
    )

    product_id = create_response.json()["id"]

    # Update only the price
    response = client.patch(
        f"/products/{product_id}",
        json={"price": 1800}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["price"] == 1800
    assert data["name"] == "Gaming Mouse"
    assert data["quantity"] == 10

def test_delete_product(client):
    # Create a product
    create_response = client.post(
        "/products/",
        json={
            "name": "Test Monitor",
            "price": 15000,
            "quantity": 4,
            "category": "Electronics"
        }
    )

    product_id = create_response.json()["id"]

    # Delete the product
    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"

    # Confirm the product no longer exists
    get_response = client.get(f"/products/{product_id}")

    assert get_response.status_code == 404

def test_create_product_with_negative_price(client):
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "price": -100,
            "quantity": 5,
            "category": "Electronics"
        }
    )

    assert response.status_code == 422

def test_create_product_without_name(client):
    response = client.post(
        "/products/",
        json={
            "price": 500,
            "quantity": 5,
            "category": "Electronics"
        }
    )

    assert response.status_code == 422

def test_get_nonexistent_product(client):
    response = client.get("/products/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_update_nonexistent_product(client):
    response = client.patch(
        "/products/99999",
        json={
            "price": 1500
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_delete_nonexistent_product(client):
    response = client.delete("/products/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_search_products_by_name(client):
    # Create two products
    client.post(
        "/products/",
        json={
            "name": "Gaming Keyboard",
            "price": 2500,
            "quantity": 10,
            "category": "Electronics"
        }
    )

    client.post(
        "/products/",
        json={
            "name": "Office Chair",
            "price": 5000,
            "quantity": 5,
            "category": "Furniture"
        }
    )

    # Search for Gaming
    response = client.get("/products/?name=Gaming")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Gaming Keyboard"

def test_filter_products_by_category(client):
    # Create two products in different categories
    client.post(
        "/products/",
        json={
            "name": "Gaming Mouse",
            "price": 1500,
            "quantity": 10,
            "category": "Electronics"
        }
    )

    client.post(
        "/products/",
        json={
            "name": "Office Chair",
            "price": 5000,
            "quantity": 5,
            "category": "Furniture"
        }
    )

    # Filter by Electronics
    response = client.get("/products/?category=Electronics")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Gaming Mouse"
    assert data[0]["category"] == "Electronics"

def test_paginate_products(client):
    # Create three products
    for i in range(1, 4):
        client.post(
            "/products/",
            json={
                "name": f"Product {i}",
                "price": 100 * i,
                "quantity": 10,
                "category": "Electronics"
            }
        )

    # Request only two products
    response = client.get("/products/?skip=0&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

def test_paginate_products_second_page(client):
    # Create three products
    for i in range(1, 4):
        client.post(
            "/products/",
            json={
                "name": f"Product {i}",
                "price": 100 * i,
                "quantity": 10,
                "category": "Electronics"
            }
        )

    # Skip the first two products and get the next two
    response = client.get("/products/?skip=2&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Product 3"
