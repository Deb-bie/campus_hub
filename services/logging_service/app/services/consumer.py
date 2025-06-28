import json
import asyncio
from kafka import KafkaConsumer # type: ignore
from app.db.db import collection
from app.schemas.schema import LogItem
from app.config import settings
import threading
import time
import logging
import os
from kafka.errors import NoBrokersAvailable # type: ignore


logger = logging.getLogger(__name__)

KAFKA_BROKER = settings.KAFKA_BROKER
KAFKA_TOPICS = settings.KAFKA_TOPICS



def wait_for_kafka(broker_url, max_retries=30, delay=2):
    """Waiting for Kafka to become available"""
    import socket
    
    host, port = broker_url.split(':')
    port = int(port)
    
    for attempt in range(max_retries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.info(f"Kafka is available at {broker_url}")
                return True
            else:
                logger.info(f"Waiting for Kafka... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
        except Exception as e:
            logger.info(f"Waiting for Kafka... (attempt {attempt + 1}/{max_retries}) - {e}")
            time.sleep(delay)
    
    logger.error(f"Kafka not available after {max_retries} attempts")
    return False

def kafka_consumer_loop():

    if not wait_for_kafka(KAFKA_BROKER):
        logger.error("Failed to connect to Kafka. Exiting.")
        return
    
    # Add additional delay to ensure Kafka is fully initialized
    logger.info("Kafka is available. Waiting 10 more seconds for full initialization...")
    time.sleep(10)
    
    max_retries = 5
    retry_delay = 5


    for attempt in range(max_retries):
        try:
            logger.info(f"Creating Kafka consumer (attempt {attempt + 1}/{max_retries})")

            consumer = KafkaConsumer(
                *KAFKA_TOPICS,
                bootstrap_servers=[KAFKA_BROKER],
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                group_id='logging-group',
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )

            logger.info("Successfully created Kafka consumer!")
            json_string = json.dumps(KAFKA_TOPICS)
            topics = json.loads(json_string)
            
            consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")

        except NoBrokersAvailable as e:
            logger.error(f"No Kafka brokers available (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Kafka connection failed.")
                raise
        except Exception as e:
            logger.error(f"Unexpected error in Kafka consumer: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

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
        try:
            logger.info(f"Received message from {message.topic}: {message.value}")
            log_data = message.value
            loop.run_until_complete(process_log_async(log_data))
        except Exception as e:
            logger.error(f"Error processing message: {e}")

def start_consumer_thread():
    thread = threading.Thread(target=kafka_consumer_loop, daemon=True)
    thread.start()

