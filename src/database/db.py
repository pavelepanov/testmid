from redis import Redis
from config import REDIS_PORT, REDIS_HOST

redis_client = Redis(host=f"{REDIS_HOST}", port=REDIS_PORT, db=0)