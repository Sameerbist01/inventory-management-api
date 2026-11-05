from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from sqlalchemy.orm import Session
from app.models.product import Product as ProductModel

#create product function
def create_product(db: Session, product: ProductCreate):
    new_product = ProductModel(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
#get product by id
def get_product_by_id(db: Session, product_id: int):
    return db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

#update product by id

def update_product(
    db: Session,
    product_id: int,
    product_update: ProductUpdate
):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if product is None:
        return None

    updated_data = product_update.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

#function to delete product by id

def delete_product(db: Session, product_id: int):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if product is None:
        return None

    db.delete(product)
    db.commit()

    return product




#pagination ,filtering and searching products
def get_products(
    db: Session,
    name: str | None = None,
    category: str | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(ProductModel)

    if name:
        query = query.filter(
            ProductModel.name.ilike(f"%{name}%")
        )

    if category:
        query = query.filter(
            ProductModel.category == category
        )

    return query.offset(skip).limit(limit).all()