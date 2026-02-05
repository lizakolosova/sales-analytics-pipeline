from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import asyncio
import json
import random

app = FastAPI(title="Sales Stream API")

class SalesEvent(BaseModel):
    transaction_id: str
    timestamp: datetime
    customer_id: str
    product_id: str
    quantity: int
    unit_price: float
    total_amount: float
    payment_method: str
    status: str

class SalesSimulator:
    def __init__(self):
        self.transaction_counter = 0
        self.products = self._load_products()
        self.customers = self._load_customers()
    
    def _load_products(self):
        try:
            with open('data/products.json', 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _load_customers(self):
        try:
            with open('data/customers.json', 'r') as f:
                return json.load(f)
        except:
            return []
    
    def generate_event(self) -> dict:
        self.transaction_counter += 1
        product = random.choice(self.products)
        customer = random.choice(self.customers)
        quantity = random.randint(1, 5)
        
        return {
            'transaction_id': f'TXN{self.transaction_counter:08d}',
            'timestamp': datetime.utcnow().isoformat(),
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': round(product['price'] * quantity, 2),
            'payment_method': random.choice(['credit_card', 'paypal', 'debit_card', 'crypto']),
            'status': random.choice(['completed', 'pending', 'failed'])
        }

simulator = SalesSimulator()

@app.get("/")
async def root():
    return {
        "service": "Sales Stream API",
        "version": "1.0.0",
        "endpoints": ["/stream", "/event", "/health"]
    }

@app.get("/event")
async def get_single_event():
    return simulator.generate_event()

@app.get("/stream")
async def stream_events(rate: Optional[int] = 1):
    async def event_generator():
        while True:
            event = simulator.generate_event()
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(1 / rate)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
