from fastapi import FastAPI, HTTPException
from .database import init_db
from . import models
from typing import Optional, List
from .converter import convert_currency
from .models import Currency
from .database_operations import (
    get_order_by_id, 
    get_all_orders, 
    create_order_in_db, 
    update_order_in_db,
)

init_db()

app = FastAPI(title="Order Management API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Order Management, visit http://127.0.0.1:8000/docs"}

@app.post("/orders", response_model=models.Order)
def create_order(order: models.OrderCreate):
    """Create new order"""
    return create_order_in_db(
        customer_name=order.customer_name, 
        price=order.price, 
        currency=order.currency.value
    )

@app.get("/orders", response_model=List[models.Order])
def get_orders(to_currency: Optional[Currency] = None):
    """Get all orders from database"""
    orders = get_all_orders()

    if to_currency:
        for order in orders:
            order["price"] = convert_currency(
                order_price=order["price"],
                from_currency=order["currency"],
                to_currency=to_currency
            )
            order["currency"] = to_currency.value

    return orders

@app.get("/orders/{order_id}", response_model=models.Order)
def get_order(order_id: int, to_currency: Optional[Currency] = None):
    """Get order by ID from database"""
    order = get_order_by_id(order_id=order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order is not found")

    if to_currency:
        order["price"] = convert_currency(
            order_price=order["price"],
            from_currency=order["currency"],
            to_currency=to_currency.value
        )
        order["currency"] = to_currency.value

    return order

@app.put("/orders/{order_id}", response_model=models.Order)
def update_order(order_id: int, order_update: models.OrderUpdate):
    """Update existing order"""
    updated_order = update_order_in_db(
        order_id=order_id,
        customer_name=order_update.customer_name,
        price=order_update.price,
        currency=order_update.currency.value
    )
    
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order is not found")
    
    return updated_order