from fastapi import FastAPI
from .database import init_db, get_db_connection
from . import models
from typing import Optional, List


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
            (order.customer_name, order.price, order.currency)
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