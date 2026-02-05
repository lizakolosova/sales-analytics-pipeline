from kafka import KafkaProducer
import json
import requests
import time
from config.settings import get_settings

settings = get_settings()

class SalesProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        self.topic = settings.KAFKA_TOPIC_SALES
    
    def send_event(self, event: dict):
        try:
            future = self.producer.send(self.topic, value=event)
            record_metadata = future.get(timeout=10)
            return {
                'topic': record_metadata.topic,
                'partition': record_metadata.partition,
                'offset': record_metadata.offset
            }
        except Exception as e:
            print(f"Error sending event: {e}")
            return None
    
    def stream_from_api(self, api_url: str = "http://localhost:8000/event", interval: float = 1.0):
        print(f"Starting to stream events to Kafka topic: {self.topic}")
        
        while True:
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    event = response.json()
                    result = self.send_event(event)
                    if result:
                        print(f"Sent: {event['transaction_id']} -> Partition {result['partition']}, Offset {result['offset']}")
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\nShutting down producer...")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)
        
        self.producer.close()

def main():
    producer = SalesProducer()
    producer.stream_from_api(interval=0.5)

if __name__ == "__main__":
    main()
