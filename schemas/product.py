from pydantic import BaseModel, Field
from typing import List, Optional

# Product size with inventory
class Size(BaseModel):
    size: str = Field(..., description="Size")
    quantity: int = Field(..., description="Quantity")
    
# Schema for creating new products
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Product name")
    price: float = Field(..., description="Product price")
    sizes: List[Size] = Field(..., min_items=1, description="Available sizes")

# Schema for product output
class ProductOut(BaseModel):
    id: str
    name: str
    price: float

# Pagination metadata
class PaginationMeta(BaseModel):
    next: int 
    limit: int 
    previous: int

# Paginated response wrapper
class PaginatedProductResponse(BaseModel):
    data: List[ProductOut]
    page: PaginationMeta
