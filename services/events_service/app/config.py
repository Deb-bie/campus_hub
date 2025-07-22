import os
from dotenv import load_dotenv # type: ignore

load_dotenv() 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Elasticsearch configuration
    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
    ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT'))
    ELASTICSEARCH_SCHEME = os.getenv('ELASTICSEARCH_SCHEME')
    ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX')

    # kafka configuration
    KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

    # Pagination defaults
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 10))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))

config = Config()