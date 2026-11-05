from pydantic import BaseModel, Field,ConfigDict,model_validator

#schema for creating product 
class ProductCreate(BaseModel):
      
      name: str = Field(...,min_length=2,max_length=100,description="Name of the product")
      price : float = Field(...,gt=0, description="Price of the product")
      quantity : int = Field(...,ge=0, description="Quantity of the product")
      category : str = Field(...,min_length=2,max_length=50, description="Category of the product")

#schema for updating product
class ProductUpdate(BaseModel):
      name:str | None = Field(default=None,min_length=2,max_length=100, description="Name of the product"
      )
      price: float | None = Field(default=None,gt=0)
      quantity: int |None = Field(default=None,ge=0,description="Quantity of the product")
      category: str |None = Field(default=None,min_length=2,max_length=50,description="Category of the product")
      @model_validator(mode="after")
      def reject_explicit_null(self):
            for field_name in self.model_fields_set:
                  if getattr(self, field_name) is None:
                        raise ValueError(f"{field_name} cannot be explicitly set to null")
            return self
#schema for returning product information
class ProductResponse(ProductCreate):
      id :int 
      model_config = ConfigDict(from_attributes=True)      


