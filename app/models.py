from pydantic import BaseModel, Field, field_validator

class OrderBase(BaseModel):
    customer_name: str
    price: float = Field(..., gt=0)
    currency: str

    @field_validator('currency')
    def currency_valid(cls, currency):
        allowed_currencies = ["CZK", "USD", "EUR"]
        if currency not in allowed_currencies:
            raise ValueError(f"Currency must to be one of allowed currencies: {allowed_currencies}")
        return currency

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

