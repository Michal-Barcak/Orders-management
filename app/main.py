from fastapi import FastAPI, HTTPException
from .database import init_db, get_db_connection
from . import models
from typing import Optional, List
from .converter import convert_currency
from .models import Currency

init_db()

app = FastAPI(title="Order Management API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Order Management"}

@app.post("/orders", response_model=models.Order, status_code=201)
def create_order(order: models.OrderCreate):
    """Create new order"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_name, price, currency) VALUES (?,?,?)",
            (order.customer_name, order.price, order.currency.value)
        )
        conn.commit()
        order_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, customer_name, price, currency FROM orders WHERE id = ?",
            (order_id,)
        )
        result = dict(cursor.fetchone())

    return result

@app.get("/orders", response_model=List[models.Order])
def get_orders(to_currency: Optional[str] = None):
    """Get all orders from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = [dict(row) for row in cursor.fetchall()]
    return orders

@app.get("/orders/{order_id}", response_model=models.Order)
def get_order(order_id: int, to_currency: Optional[Currency] = None):
    """Get order by ID """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        existing_order = cursor.fetchone()

    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order is not found")
    
    result = dict(existing_order)

    if to_currency:
        result["price"] = convert_currency(
            result["price"],
            result["currency"],
            to_currency.value
        )
        result["currency"] = to_currency.value

    return result

@app.put("/orders/{order_id}", response_model=models.Order)
def update_order(order_id: int, order_update: models.OrderUpdate):
    """Update exist order"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        existing_order = cursor.fetchone()

    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order is not found")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET customer_name = ?, price = ?, currency = ? WHERE id = ?",
            (order_update.customer_name, order_update.price, order_update.currency.value, order_id)
        )
        conn.commit()

        cursor.execute(
            "SELECT * FROM orders WHERE id = ?",
            (order_id,)
        )
        result = dict(cursor.fetchone())
    return result