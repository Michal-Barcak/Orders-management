# Order Management API

Simple FastAPI application for order management with currency conversion support.

## Description

The application provides REST API for:
- Creating new orders
- Displaying all orders
- Displaying order by ID
- Updating existing orders
- Currency conversion (CZK, USD, EUR) with current exchange rates from CNB

## Features

- **Data validation** using Pydantic
- **SQLite database** for storing orders
- **Automatic currency conversion** on display
- **Swagger documentation** at `/docs`
- **Docker support** for easy deployment

## Requirements

- Linux
- Python 3.10+
- Optional - Docker and Docker Compose (for Docker deployment)

## Running the Application

### Option 1: Local deployment (without Docker)

1. **Create virtual environment:**
    - `python3 -m venv venv`
    - `source venv/bin/activate`

2. **Install dependencies:**
    - `pip install -r requirements.txt`

3. **Run application:**
    - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`


4. **Access application:**
    - API: http://localhost:8000
    - Swagger documentation: http://localhost:8000/docs

### Option 2: Docker deployment (recommended)

#### First Docker installation (one time only)

1. **Install Docker:**
    - `sudo apt update`
    - `sudo apt install docker.io docker-compose`

2. **Start Docker service:**
    - `sudo systemctl start docker`
    - `sudo systemctl enable docker`

3. **Add user to docker group:**
    - `sudo usermod -aG docker $USER`
    - `newgrp docker`

4. **Verify installation:**
    - `docker --version`
    - `docker-compose --version`


#### Running the application

1. **Deactivate virtual environment (if active):**
    - `deactivate`

2. **Run application:**
    - Navigate to project directory and run: `docker-compose up --build`

3. **Access application:**
    - API: http://localhost:8000
    - Swagger documentation: http://localhost:8000/docs

4. **Stop application:**
    - `docker-compose down`


## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| POST | `/orders` | Create new order |
| GET | `/orders` | List all orders |
| GET | `/orders/{id}` | Get order by ID |
| PUT | `/orders/{id}` | Update order |

### Query parameters

- `to_currency` (optional): Convert to currency (CZK, USD, EUR)

### Example
```
GET /orders/1
{
    "id": 1,
    "customer_name": "John Doe",
    "price": 99.99,
    "currency": "CZK"
}

GET /orders/1?to_currency=EUR
{
    "id": 1,
    "customer_name": "John Doe",
    "price": 4.01,
    "currency": "EUR"
}
```


## Project Structure
    Change_currency/
    ├── app/
    │ ├── init.py
    │ ├── main.py
    │ ├── models.py
    │ ├── database.py
    │ ├── converter.py
    │ └── database_operations.py
    ├── Dockerfile
    ├── .gitignore
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md

## Technologies

- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **SQLite** - Database
- **Uvicorn** - ASGI server
- **Docker** - Containerization
- **CNB API** - Current exchange rates `https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt`


