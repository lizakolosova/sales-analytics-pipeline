import json
import logging
from datetime import datetime
from typing import Any, Dict
from functools import wraps
import time

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def serialize_datetime(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def safe_json_loads(data: str) -> Dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}

def safe_json_dumps(data: Dict) -> str:
    try:
        return json.dumps(data, default=serialize_datetime)
    except Exception:
        return "{}"

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(delay * attempts)
            return None
        return wrapper
    return decorator

def calculate_metrics(transactions: list) -> Dict[str, float]:
    if not transactions:
        return {
            'total_revenue': 0.0,
            'avg_transaction': 0.0,
            'transaction_count': 0,
            'conversion_rate': 0.0
        }
    
    completed = [t for t in transactions if t.get('status') == 'completed']
    
    total_revenue = sum(t.get('total_amount', 0) for t in completed)
    transaction_count = len(completed)
    avg_transaction = total_revenue / transaction_count if transaction_count > 0 else 0
    conversion_rate = (len(completed) / len(transactions)) * 100 if transactions else 0
    
    return {
        'total_revenue': round(total_revenue, 2),
        'avg_transaction': round(avg_transaction, 2),
        'transaction_count': transaction_count,
        'conversion_rate': round(conversion_rate, 2)
    }

def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"

def validate_transaction(transaction: Dict) -> bool:
    required_fields = [
        'transaction_id', 'customer_id', 'product_id',
        'quantity', 'unit_price', 'total_amount'
    ]
    return all(field in transaction for field in required_fields)

class Timer:
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        elapsed = time.time() - self.start_time
        print(f"{self.name} took {elapsed:.2f} seconds")
