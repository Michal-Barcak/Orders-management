import csv
import requests
from typing import Dict
from fastapi import HTTPException
from .models import Currency

BASE_CURRENCY = Currency.CZK
DEFAULT_RATES = {
    Currency.CZK.value: 1.0,
    Currency.USD.value: 22.0,
    Currency.EUR.value: 25.0
}

def get_exchange_rates() -> Dict[str, float]:
    """Get actual currency rates from CNB or default rates."""
    rates = DEFAULT_RATES.copy()
    
    try:
        url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"
        response = requests.get(url)
        lines = response.text.strip().split('\n')[2:]
        reader = csv.DictReader(lines, delimiter='|', fieldnames=['Country', 'Name', 'Amount', 'Code', 'Rate'])
        
        for row in reader:
            code = row['Code'].strip()
            if code in [c.value for c in Currency]:
                rate = float(row['Rate'].replace(',', '.'))
                amount = int(row['Amount'])
                rates[code] = rate / amount
    
    except Exception as e:
        print(f"Error during loading rates: {str(e)}")
    
    return rates

def convert_currency(order_price: float, from_currency: str, to_currency: str) -> float:
    """
    Function for converting currency from one to another.
    """
    if from_currency == to_currency:
        return order_price
    
    try:
        rates = get_exchange_rates()

        base_price = order_price
        #  If source currency is not CZK (BASE_CURRENCY), convert it to CZK first
        if from_currency != BASE_CURRENCY:
            base_price = order_price * rates[from_currency]
        
        if to_currency == BASE_CURRENCY:
            result = base_price
        elif to_currency in rates:
            result = base_price / rates[to_currency]
        else:
            raise ValueError(f"Unsupported currency: {to_currency}")
            
        return round(result, 3)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during currency conversion: {str(e)}"
        )

