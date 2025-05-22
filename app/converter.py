import csv
import requests
# from functools import lru_cache
from typing import Dict
from fastapi import HTTPException
from .models import Currency

BASE_CURRENCY = Currency.CZK
DEFAULT_RATES = {
    Currency.CZK.value: 1.0,
    Currency.USD.value: 22.0,
    Currency.EUR.value: 25.0
}

# @lru_cache(maxsize=1)
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

def convert_currency(price: float, from_currency: str, to_currency: str) -> float:
    """
    Convert currency from one to another.
    """
    if not to_currency or from_currency == to_currency:
        return price
    
    try:
        rates = get_exchange_rates()
        
        base_price = price
        if from_currency != BASE_CURRENCY:
            base_price = price * rates[from_currency]
        
        if to_currency == BASE_CURRENCY:
            result = base_price
        else:
            result = base_price / rates[to_currency]
            
        return round(result, 2)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during currency conversion: {str(e)}"
        )

