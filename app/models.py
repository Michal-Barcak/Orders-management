from pydantic import BaseModel, Field, field_validator

class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    currency: str = Field(..., min_length=1)

    @field_validator('currency')
    def currency_valid(cls, currency):
        allowed_currencies = ["CZK", "USD", "EUR"]
        if currency not in allowed_currencies:
            raise ValueError(f"Currency must to be one of allowed currencies: {allowed_currencies}")
        return currency
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_name": "John Doe",
                "price": 99.99,
                "currency": "CZK",
                "id": 1
            }
        }
    }

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

