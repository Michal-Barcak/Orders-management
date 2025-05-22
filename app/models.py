from pydantic import BaseModel, Field, field_validator
from enum import Enum

class Currency(str, Enum):
    """Supported currencies"""
    CZK = "CZK"
    USD = "USD"
    EUR = "EUR"

class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=100000)
    currency: Currency

    @field_validator('price')
    @classmethod
    def round_price(cls, price):
        return round(price, 3)
    
    @field_validator('customer_name')
    @classmethod
    def validate_customer_name(cls, customer_name):
        if not customer_name.strip():
            raise ValueError('Customer name cannot be empty or whitespace only')
        return customer_name.strip()

    
    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_name": "John Doe",
                "price": 99.99,
                "currency": "CZK",
            }
        }
    }

class Order(OrderBase):
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "price": 99.99,
                "currency": "CZK"
            }
        }
    }

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass
