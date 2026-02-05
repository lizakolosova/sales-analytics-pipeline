from sqlalchemy.orm import Session
from sqlalchemy import func, text
from src.database.models import Transaction, Product, Customer, SalesMetric
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class DatabaseOperations:
    def __init__(self, session: Session):
        self.session = session
    
    def bulk_insert_transactions(self, transactions: List[Dict]):
        transaction_objects = [
            Transaction(**txn) for txn in transactions
        ]
        self.session.bulk_save_objects(transaction_objects)
        self.session.commit()
    
    def get_recent_transactions(self, limit: int = 100) -> List[Transaction]:
        return self.session.query(Transaction)\
            .order_by(Transaction.timestamp.desc())\
            .limit(limit)\
            .all()
    
    def get_revenue_by_period(self, period: str = 'hour', hours: int = 24):
        if period == 'hour':
            truncate = func.date_trunc('hour', Transaction.timestamp)
        elif period == 'day':
            truncate = func.date_trunc('day', Transaction.timestamp)
        else:
            truncate = Transaction.timestamp
        
        return self.session.query(
            truncate.label('period'),
            func.count(Transaction.transaction_id).label('count'),
            func.sum(Transaction.total_amount).label('revenue')
        ).filter(
            Transaction.timestamp >= datetime.utcnow() - timedelta(hours=hours)
        ).group_by('period').order_by('period').all()
    
    def get_top_products(self, limit: int = 10):
        return self.session.query(
            Product.name,
            Product.category,
            func.count(Transaction.transaction_id).label('sales_count'),
            func.sum(Transaction.total_amount).label('revenue')
        ).join(
            Transaction,
            Transaction.product_id == Product.product_id
        ).group_by(
            Product.name,
            Product.category
        ).order_by(
            func.sum(Transaction.total_amount).desc()
        ).limit(limit).all()
    
    def get_customer_lifetime_value(self, customer_id: str) -> float:
        result = self.session.query(
            func.sum(Transaction.total_amount)
        ).filter(
            Transaction.customer_id == customer_id,
            Transaction.status == 'completed'
        ).scalar()
        
        return float(result) if result else 0.0
    
    def calculate_conversion_rate(self) -> float:
        total = self.session.query(Transaction).count()
        completed = self.session.query(Transaction)\
            .filter(Transaction.status == 'completed')\
            .count()
        
        return (completed / total * 100) if total > 0 else 0.0
    
    def get_sales_by_category(self):
        return self.session.query(
            Product.category,
            func.count(Transaction.transaction_id).label('count'),
            func.sum(Transaction.total_amount).label('revenue')
        ).join(
            Transaction,
            Transaction.product_id == Product.product_id
        ).filter(
            Transaction.status == 'completed'
        ).group_by(
            Product.category
        ).all()
    
    def save_metric(self, metric_name: str, metric_value: float, dimension: Optional[str] = None):
        metric = SalesMetric(
            timestamp=datetime.utcnow(),
            metric_name=metric_name,
            metric_value=metric_value,
            dimension=dimension
        )
        self.session.add(metric)
        self.session.commit()
    
    def cleanup_old_data(self, days: int = 30):
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        self.session.query(Transaction)\
            .filter(Transaction.timestamp < cutoff_date)\
            .delete()
        self.session.commit()
