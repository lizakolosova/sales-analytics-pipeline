import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sqlalchemy import create_engine
from config.settings import get_settings


def main():
    settings = get_settings()
    engine = create_engine(settings.database_url)

    print('Loading sample data into PostgreSQL...\n')

    try:
        data_dir = project_root / 'data'

        print('Loading products...')
        products = pd.read_csv(data_dir / 'products.csv')
        products.to_sql('products', engine, if_exists='replace', index=False)
        print(f'Loaded {len(products)} products')

        print('Loading customers...')
        customers = pd.read_csv(data_dir / 'customers.csv')
        customers.to_sql('customers', engine, if_exists='replace', index=False)
        print(f'Loaded {len(customers)} customers')

        print('Loading transactions...')
        transactions = pd.read_csv(data_dir / 'transactions.csv')
        transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
        transactions.to_sql('transactions', engine, if_exists='replace', index=False)
        print(f'Loaded {len(transactions)} transactions')

        total_revenue = transactions['total_amount'].sum()
        print(f'\nDataset Summary:')
        print(f'Total Revenue: ${total_revenue:,.2f}')
        print(f'Products: {len(products)}')
        print(f'Customers: {len(customers)}')
        print(f'Transactions: {len(transactions)}')

        print('\nData loaded successfully!')
        print('Access dashboard at http://localhost:8501')

    except FileNotFoundError as e:
        print(f'\nError: Data files not found')
        print(f'Run this first: python scripts/generate_dataset.py')
    except Exception as e:
        print(f'\nError loading data: {e}')
        print(f'Make sure Docker PostgreSQL is running:')
        print(f'docker-compose up -d postgres')


if __name__ == '__main__':
    main()