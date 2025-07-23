from kafka import KafkaProducer
import json
from app.config import config
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_event(event_type, message, payload):
    message = {
        "timestamp": datetime.now().isoformat(),
        "service_name": "events_service",
        "log_level": "INFO",
        "type": event_type,
        "message": message,
        "metadata": payload

    }
    producer.send(event_type, message)
    producer.flush()
