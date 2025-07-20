from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
import re

from database.database import products_collection
from schemas.product import ProductCreate,  PaginatedProductResponse, ProductOut, PaginationMeta

# Product routes with prefix
router = APIRouter(prefix="/anshdeep/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate):
    # Insert new product into MongoDB
    result =  products_collection.insert_one(product_data.dict())
    
    if result.inserted_id:
        created_product =  products_collection.find_one({"_id": result.inserted_id})
        return {"id":str(created_product["_id"])}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create product"
    )

@router.get("/", response_model=PaginatedProductResponse, status_code=status.HTTP_200_OK)
async def get_products(
    name: Optional[str] = Query(None, description="Filter by name (regex)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: Optional[int] = Query(0, ge=0, description="Number of items to skip")
):
    # Build query filters
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Case-insensitive search
    
    if size:
        query["sizes.size"] = size
    
    # Fetch products with pagination
    cursor = products_collection.find(query).sort("_id", 1).skip(offset if offset is not None else 0 ).limit(limit if limit is not None else 10 )
    products = []
    
    # Convert MongoDB documents to response format
    for product in cursor:
        products.append(ProductOut(
            id=str(product["_id"]),
            name=product["name"],
            price=product["price"]
        ))
    
    # Calculate pagination metadata
    next_offset = str(offset + limit)
    previous_offset = offset - limit if offset - limit >= 0 else -10
    
    pagination = PaginationMeta(
        next=next_offset,
        limit=limit,
        previous=previous_offset
    )
    
    return PaginatedProductResponse(data=products, page=pagination)