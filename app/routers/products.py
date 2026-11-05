
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service
from app.database.connection import get_db


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create a new product
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return product_service.create_product(db, product)


# Get all products
@router.get("/", response_model=list[ProductResponse])
def get_products(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return product_service.get_products(
        db=db,
        name=name,
        category=category,
        skip=skip,
        limit=limit
    )


# Get single product by ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = product_service.get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# Delete product by ID (still using old in-memory service)

# Delete product by ID
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    deleted_product = product_service.delete_product(db, product_id)

    if deleted_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully",
        "deleted_product": deleted_product
    }


# Partial update product by ID
@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    updated_product = product_service.update_product(
        db,
        product_id,
        product_update
    )

    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return updated_product
