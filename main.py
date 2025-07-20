from fastapi import FastAPI
import uvicorn
from routes import products, orders

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Hr one backend apis",
    description="FastAPI backend for hrone task  with MongoDB",
    version="1.0.0",
)

# Register route handlers
app.include_router(products.router)
app.include_router(orders.router)

# Root endpoint for API health check
@app.get("/")
async def root():
    return {"message": "Welcome to hrone API", "version": "1.0.0"}

# Run server locally for development
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)