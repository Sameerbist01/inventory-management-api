from fastapi import FastAPI
from app.routers import products
from app.database.connection import engine, Base
from app.models import Product

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API" ,description="API for managing inventory items, including adding, updating, and retrieving item details.", version="1.0.0")

#Include the products router
app.include_router(products.router)




#home root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the Inventory Management API!",
        "status": "API is running successfully."
        }


#check the health endpoint
@app.get("/health"
         )
def health_check():
    return {
        "status": "healthy"
        }