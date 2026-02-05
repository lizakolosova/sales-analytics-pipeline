from kafka import KafkaConsumer
import json
from config.settings import get_settings

settings = get_settings()

class SalesConsumer:
    def __init__(self, group_id: str = "sales-analytics-group"):
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_SALES,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def consume(self, callback=None):
        print(f"Starting consumer... Listening to {settings.KAFKA_TOPIC_SALES}")
        
        try:
            for message in self.consumer:
                event = message.value
                print(f"Consumed: {event['transaction_id']} - ${event['total_amount']}")
                
                if callback:
                    callback(event)
        
        except KeyboardInterrupt:
            print("\nShutting down consumer...")
        finally:
            self.consumer.close()

def main():
    consumer = SalesConsumer()
    consumer.consume()

if __name__ == "__main__":
    main()
