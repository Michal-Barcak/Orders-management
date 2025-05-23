from .database import get_db_connection
from typing import Optional, Dict, List

def get_order_by_id(order_id: int) -> Optional[Dict]:
    """Get single order by ID from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        return dict(order) if order else None

def get_all_orders() -> List[Dict]:
    """Get all orders from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        return [dict(row) for row in cursor.fetchall()]

def create_order_in_db(customer_name: str, price: float, currency: str) -> Dict:
    """Create new order in database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_name, price, currency) VALUES (?,?,?)",
            (customer_name, price, currency)
        )
        conn.commit()
        order_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, customer_name, price, currency FROM orders WHERE id = ?",
            (order_id,)
        )
        return dict(cursor.fetchone())

def update_order_in_db(order_id: int, customer_name: str, price: float, currency: str) -> Optional[Dict]:
    """Update existing order in database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
        if cursor.fetchone() is None:
            return None
            
        cursor.execute(
            "UPDATE orders SET customer_name = ?, price = ?, currency = ? WHERE id = ?",
            (customer_name, price, currency, order_id)
        )
        conn.commit()

        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        return dict(cursor.fetchone())

