from pydantic import BaseModel, Field
from typing import List, Optional

from schemas.product import PaginationMeta

# Order item input
class Item(BaseModel):
    productId: str = Field(..., description="Product ID")
    qty: int = Field(..., description="Quantity")

# Schema for creating new orders
class OrderCreate(BaseModel):
    userId: str = Field(..., min_length=1, description="User ID")
    items: List[Item] = Field(..., min_items=1, description="List of product IDs and quantity")

# Product info for order display
class ProductDetails(BaseModel):
    id: str
    name: str

# Order item with product details
class OrderItem(BaseModel):
    productDetails: ProductDetails
    qty: int

# Order output with calculated total
class OrderOut(BaseModel):
    id: str 
    items: List[OrderItem]
    total: float

# Paginated order response
class PaginatedOrderResponse(BaseModel):
    data: List[OrderOut]
    page: PaginationMeta
