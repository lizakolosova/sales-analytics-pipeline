import pandas as pd
from sqlalchemy import create_engine
from config.settings import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

print('Loading sample data into PostgreSQL...')

products = pd.read_csv('data/products.csv')
products.to_sql('products', engine, if_exists='replace', index=False)
print(f'Loaded {len(products)} products')

customers = pd.read_csv('data/customers.csv')
customers.to_sql('customers', engine, if_exists='replace', index=False)
print(f'Loaded {len(customers)} customers')

transactions = pd.read_csv('data/transactions.csv')
transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
transactions.to_sql('transactions', engine, if_exists='replace', index=False)
print(f'Loaded {len(transactions)} transactions')

print('\n Data loaded! Access dashboard at http://localhost:8501')