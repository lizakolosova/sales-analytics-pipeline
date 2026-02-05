from datetime import datetime

from src.utils.helpers import (
    calculate_metrics,
    format_currency,
    validate_transaction,
    safe_json_loads,
    safe_json_dumps
)


def test_calculate_metrics():
    transactions = [
        {'total_amount': 100.0, 'status': 'completed'},
        {'total_amount': 200.0, 'status': 'completed'},
        {'total_amount': 150.0, 'status': 'failed'},
    ]
    
    metrics = calculate_metrics(transactions)
    
    assert metrics['total_revenue'] == 300.0
    assert metrics['transaction_count'] == 2
    assert metrics['avg_transaction'] == 150.0
    assert abs(metrics['conversion_rate'] - 66.67) < 0.1

def test_calculate_metrics_empty():
    metrics = calculate_metrics([])
    
    assert metrics['total_revenue'] == 0.0
    assert metrics['transaction_count'] == 0
    assert metrics['conversion_rate'] == 0.0

def test_format_currency():
    assert format_currency(1000) == "$1,000.00"
    assert format_currency(1234.56) == "$1,234.56"
    assert format_currency(0.99) == "$0.99"

def test_validate_transaction():
    valid_txn = {
        'transaction_id': 'TXN001',
        'customer_id': 'CUST001',
        'product_id': 'PRD001',
        'quantity': 1,
        'unit_price': 100.0,
        'total_amount': 100.0
    }
    
    invalid_txn = {
        'transaction_id': 'TXN001',
        'customer_id': 'CUST001'
    }
    
    assert validate_transaction(valid_txn) is True
    assert validate_transaction(invalid_txn) is False

def test_safe_json_loads():
    valid_json = '{"key": "value"}'
    invalid_json = '{invalid json}'
    
    assert safe_json_loads(valid_json) == {"key": "value"}
    assert safe_json_loads(invalid_json) == {}

def test_safe_json_dumps():
    data = {"key": "value", "timestamp": datetime(2024, 1, 1)}
    result = safe_json_dumps(data)
    
    assert '"key": "value"' in result
    assert '2024-01-01' in result
