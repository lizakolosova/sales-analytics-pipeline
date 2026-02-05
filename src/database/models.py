from sqlalchemy import Column, String, Integer, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    country = Column(String)
    city = Column(String)
    signup_date = Column(DateTime)

class Transaction(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    customer_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String)
    status = Column(String)

class SalesMetric(Base):
    __tablename__ = 'sales_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    dimension = Column(String)

def get_engine(database_url: str):
    return create_engine(database_url)

def get_session(engine):
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

def init_db(database_url: str):
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)
    return engine
