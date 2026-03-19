from abc import ABC, abstractmethod
import json
import redis
from kafka import KafkaProducer

class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data):
        pass

    def close(self):
        pass

class ConsoleOutput(OutputStrategy):
    def write(self, data):
        for row in data:
            print(row)

class RedisOutput(OutputStrategy):
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.client.ping()
        print("Connected to Redis")

    def write(self, data):
        for row in data:
            case_id = row.get(list(row.keys())[0], 'Unknown').strip('"')
            self.client.set(f"case:{case_id}", json.dumps(row, ensure_ascii=False))
            print(f"Data saved to Redis: case:{case_id}")

    def close(self):
        pass

class KafkaOutput(OutputStrategy):
    def __init__(self, bootstrap_servers='localhost:9092', topic='sf_311_cases'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )
        self.topic = topic
        print("Connected to Kafka")

    def write(self, data):
        for row in data:
            case_id = row.get(list(row.keys())[0], 'Unknown').strip('"')
            self.producer.send(self.topic, row)
            self.producer.flush()  
            print(f"Data sent to Kafka: {case_id}")

    def close(self):
        self.producer.flush()
        self.producer.close()