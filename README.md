# HR One Backend API

FastAPI-based REST API for Hrone task  operations with MongoDB integration.

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **MongoDB** - NoSQL database for data storage
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **Docker** - Containerization support

## Project Structure

```
hronebackend/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore rules
├── .dockerignore         # Docker ignore rules
├── database/
│   ├── __init__.py
│   └── database.py       # MongoDB connection setup
├── routes/
│   ├── __init__.py
│   ├── products.py       # Product endpoints
│   └── orders.py         # Order endpoints
└── schemas/
    ├── __init__.py
    ├── product.py        # Product data models
    └── order.py          # Order data models
```

## Installation

### Local Setup

1. Clone the repository
```bash
git clone <repository-url>
cd hronebackend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file with MongoDB connection
```env
MONGO_URL=mongodb://localhost:27017/hronedb
```

5. Run the application
```bash
python main.py
```

### Docker Setup


1. Or build Docker image manually
```bash
docker build -t hr-one-backend .
docker run -p 8000:8000 --env-file .env hr-one-backend
```

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Products

#### Create Product
- **POST** `/anshdeep/products/`
- **Body:**
```json
{
  "name": "T-Shirt",
  "price": 29.99,
  "sizes": [
    {"size": "S", "quantity": 10},
    {"size": "M", "quantity": 15},
    {"size": "L", "quantity": 20}
  ]
}
```
- **Response:**
```json
{
  "id": "507f1f77bcf86cd799439011"
}
```

#### Get Products (with pagination and filters)
- **GET** `/anshdeep/products/`
- **Query Parameters:**
  - `name` (optional): Filter by name (regex search)
  - `size` (optional): Filter by available size
  - `limit` (optional): Items per page (default: 10, max: 100)
  - `offset` (optional): Items to skip (default: 0)
- **Response:**
```json
{
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "T-Shirt",
      "price": 29.99
    }
  ],
  "page": {
    "next": 10,
    "limit": 10,
    "previous": -10
  }
}
```

### Orders

#### Create Order
- **POST** `/anshdeep/orders/`
- **Body:**
```json
{
  "userId": "user123",
  "items": [
    {"productId": "507f1f77bcf86cd799439011", "qty": 2},
    {"productId": "507f1f77bcf86cd799439012", "qty": 1}
  ]
}
```
- **Response:**
```json
{
  "id": "507f1f77bcf86cd799439013"
}
```

#### Get User Orders
- **GET** `/anshdeep/orders/{user_id}`
- **Path Parameters:**
  - `user_id`: The user's ID
- **Query Parameters:**
  - `limit` (optional): Items per page (default: 10, max: 100)
  - `offset` (optional): Items to skip (default: 0)
- **Response:**
```json
{
  "data": [
    {
      "id": "507f1f77bcf86cd799439013",
      "items": [
        {
          "productDetails": {
            "id": "507f1f77bcf86cd799439011",
            "name": "T-Shirt"
          },
          "qty": 2
        }
      ],
      "total": 59.98
    }
  ],
  "page": {
    "next": 10,
    "limit": 10,
    "previous": -10
  }
}
```

### Health Check
- **GET** `/`
- **Response:**
```json
{
  "message": "Welcome to hrone API",
  "version": "1.0.0"
}
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| MONGO_URL | MongoDB connection string | Required |



## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error
