import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Transaction, Product
from src.database.operations import DatabaseOperations
from datetime import datetime

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def sample_transactions():
    return [
        {
            'transaction_id': 'TXN001',
            'timestamp': datetime.utcnow(),
            'customer_id': 'CUST001',
            'product_id': 'PRD001',
            'quantity': 2,
            'unit_price': 100.0,
            'total_amount': 200.0,
            'payment_method': 'credit_card',
            'status': 'completed'
        }
    ]

def test_bulk_insert_transactions(db_session, sample_transactions):
    ops = DatabaseOperations(db_session)
    ops.bulk_insert_transactions(sample_transactions)
    
    count = db_session.query(Transaction).count()
    assert count == 1

def test_get_recent_transactions(db_session, sample_transactions):
    ops = DatabaseOperations(db_session)
    ops.bulk_insert_transactions(sample_transactions)
    
    transactions = ops.get_recent_transactions(limit=10)
    assert len(transactions) == 1
    assert transactions[0].transaction_id == 'TXN001'

def test_calculate_conversion_rate(db_session):
    ops = DatabaseOperations(db_session)
    
    transactions = [
        {
            'transaction_id': f'TXN{i:03d}',
            'timestamp': datetime.utcnow(),
            'customer_id': 'CUST001',
            'product_id': 'PRD001',
            'quantity': 1,
            'unit_price': 100.0,
            'total_amount': 100.0,
            'payment_method': 'credit_card',
            'status': 'completed' if i < 8 else 'failed'
        }
        for i in range(10)
    ]
    
    ops.bulk_insert_transactions(transactions)
    conversion_rate = ops.calculate_conversion_rate()
    
    assert conversion_rate == 80.0

def test_save_metric(db_session):
    ops = DatabaseOperations(db_session)
    ops.save_metric('daily_revenue', 15000.0, 'sales')
    
    from src.database.models import SalesMetric
    metric = db_session.query(SalesMetric).first()
    
    assert metric is not None
    assert metric.metric_name == 'daily_revenue'
    assert metric.metric_value == 15000.0
