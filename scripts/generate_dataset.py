import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random
from pathlib import Path

np.random.seed(41)
random.seed(41)

FIRST_NAMES = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Chris', 'Anna', 'Robert', 'Lisa']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
          'Dallas', 'San Jose']
COUNTRIES = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Spain', 'Italy', 'Australia', 'Japan', 'Brazil']
PRODUCT_NAMES = ['Pro X', 'Elite', 'Premium', 'Standard', 'Plus', 'Max', 'Ultra', 'Basic', 'Advanced', 'Classic']


def get_data_dir():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir


def generate_products(n=100):
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys']
    products = []

    for i in range(n):
        category = random.choice(categories)
        products.append({
            'product_id': f'PRD{i:05d}',
            'name': f'{random.choice(PRODUCT_NAMES)} {category} {i}',
            'category': category,
            'price': round(np.random.uniform(10, 1000), 2),
            'cost': round(np.random.uniform(5, 500), 2)
        })

    return pd.DataFrame(products)


def generate_customers(n=1000):
    customers = []

    for i in range(n):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        customers.append({
            'customer_id': f'CUST{i:06d}',
            'name': f'{first_name} {last_name}',
            'email': f'{first_name.lower()}.{last_name.lower()}{i}@email.com',
            'country': random.choice(COUNTRIES),
            'city': random.choice(CITIES),
            'signup_date': str((datetime.now() - timedelta(days=random.randint(0, 730))).date())
        })

    return pd.DataFrame(customers)


def generate_transactions(products_df, customers_df, n=10000):
    transactions = []

    for i in range(n):
        product = products_df.sample(1).iloc[0]
        customer = customers_df.sample(1).iloc[0]
        quantity = np.random.randint(1, 6)
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)

        transactions.append({
            'transaction_id': f'TXN{i:08d}',
            'timestamp': str(datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)),
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': round(product['price'] * quantity, 2),
            'payment_method': np.random.choice(['credit_card', 'paypal', 'debit_card', 'crypto']),
            'status': np.random.choice(['completed', 'pending', 'failed'], p=[0.85, 0.10, 0.05])
        })

    return pd.DataFrame(transactions)


def main():
    data_dir = get_data_dir()
    print(f"Data directory: {data_dir}")

    print("Generating products...")
    products = generate_products(100)
    products.to_csv(data_dir / 'products.csv', index=False)
    products.to_json(data_dir / 'products.json', orient='records', indent=2)

    print("Generating customers...")
    customers = generate_customers(1000)
    customers.to_csv(data_dir / 'customers.csv', index=False)
    customers.to_json(data_dir / 'customers.json', orient='records', indent=2)

    print("Generating transactions...")
    transactions = generate_transactions(products, customers, 10000)
    transactions.to_csv(data_dir / 'transactions.csv', index=False)
    transactions.to_json(data_dir / 'transactions.json', orient='records', indent=2)

    print(f"\nDataset Summary:")
    print(f"Products: {len(products)}")
    print(f"Customers: {len(customers)}")
    print(f"Transactions: {len(transactions)}")
    print(f"Total Revenue: ${transactions['total_amount'].sum():,.2f}")
    print(f"\nFiles saved to: {data_dir}")


if __name__ == '__main__':
    main()