import json
import asyncio
from kafka import KafkaConsumer # type: ignore
from app.db.db import collection
from app.schemas.schema import LogItem
from app.config import settings
import threading

KAFKA_BROKER = settings.KAFKA_BROKER
KAFKA_TOPICS = settings.KAFKA_TOPICS


def kafka_consumer_loop():
    consumer = KafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id='logging-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    async def process_log_async(log_data):
        try:
            log = LogItem(**log_data)
            print("printing log :", log)
            await collection.insert_one(log.dict())
            print(f"Inserted log from {log.service_name}: {log.message}")
        except Exception as e:
            print(f"Error inserting log: {e}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for message in consumer:
        log_data = message.value
        loop.run_until_complete(process_log_async(log_data))

def start_consumer_thread():
    thread = threading.Thread(target=kafka_consumer_loop, daemon=True)
    thread.start()

