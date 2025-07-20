from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import List, Optional
from bson import ObjectId

from database.database import orders_collection, products_collection
from schemas.order import OrderCreate, OrderItem, OrderOut, PaginatedOrderResponse, ProductDetails
from schemas.product import PaginationMeta

# Order routes with prefix
router = APIRouter(prefix="/anshdeep/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    # Validate all product IDs exist before creating order
    product_ids = []
    for pid in order_data.items:
        try:
            obj_id = ObjectId(pid.productId)
            product =  products_collection.database.products.find_one({"_id": obj_id})
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {pid} not found"
                )
            product_ids.append(pid)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid product ID: {pid}"
            )
    
    # Insert order into MongoDB
    result =  orders_collection.insert_one(order_data.dict())
    
    if result.inserted_id:
        created_order =  orders_collection.find_one({"_id": result.inserted_id})
        return {"id":str(created_order["_id"])}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create order"
    )

@router.get("/{user_id}", response_model=PaginatedOrderResponse, status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: str = Path(..., description="User ID"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of items per page") ,
    offset: Optional[int] = Query(0, ge=0, description="Number of items to skip")
):
    # Fetch orders for specific user with pagination
    cursor = orders_collection.find({"userId": user_id}).skip(offset if offset is not None else 0 ).limit(limit if limit is not None else 10 )
    orders = []
    
    # Process each order and fetch product details
    for order in cursor:
        order_items = []
        total = 0
        # Calculate order total and fetch product info
        for item in order["items"]:
            product =  products_collection.find_one({"_id": ObjectId(item["productId"])})
            if product:
                order_items.append(OrderItem(
                    productDetails=ProductDetails(
                        name=product["name"],
                        id=str(product["_id"])
                    ),
                    qty=item["qty"]
                ))
                total += product["price"] * item["qty"]
        
        orders.append(OrderOut(
            id=str(order["_id"]),
            items=order_items,
            total=total
        ))
    
    # Calculate pagination metadata
    next_offset = str(offset + limit)
    previous_offset = offset - limit if offset - limit >= 0 else -10
    
    page_info = PaginationMeta(
        next=next_offset,
        limit=limit,
        previous=previous_offset
    )
    
    return PaginatedOrderResponse(data=orders, page=page_info)