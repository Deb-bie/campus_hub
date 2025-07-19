from app.__init__ import create_app
from dotenv import load_dotenv # type: ignore
import os
from app import redis_client

load_dotenv()

app = create_app()

redis_client.redis_client

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=os.getenv("PORT"),
        debug=True
    )