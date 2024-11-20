import redis
import json
from typing import List, Dict
from datetime import datetime

class RedisManager:
    def __init__(self, host: str = 'localhost', port: int = 6380, db: int = 0):
        """
        Initializes the Redis connection.
        
        :param host: Redis server hostname
        :param port: Redis server port
        :param db: Redis database index
        """
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def set_message(self, chat_session_id: str, message) -> None:
        """
        Stores a message for a session in Redis.
        
        :param chat_session_id: The unique identifier for the session
        :param message: The message to store (dictionary with 'role' and 'content')
        """
        try:
            # Serialize the dictionary as a JSON string before storing it in Redis
            self.client.rpush(chat_session_id, json.dumps(message))
        except redis.RedisError as e:
            print(f"Error storing message: {str(e)}")

    def get_messages(self, chat_session_id: str) -> List[Dict[str, str]]:
        """
        Retrieves all messages for a session from Redis.
        
        :param chat_session_id: The unique identifier for the session
        :return: A list of messages as dictionaries
        """
        try:
            messages = self.client.lrange(chat_session_id, 0, -1)
            # Deserialize each message from JSON string to a dictionary
            return [json.loads(msg) for msg in messages]
        except redis.RedisError as e:
            print(f"Error retrieving messages: {str(e)}")
            return []

    def delete_session(self, chat_session_id: str) -> None:
        """
        Deletes all messages for a session.
        
        :param chat_session_id: The unique identifier for the session
        """
        try:
            self.client.delete(chat_session_id)
        except redis.RedisError as e:
            print(f"Error deleting session: {str(e)}")

    def set_session_expiry(self, chat_session_id: str, expiry: datetime) -> None:
        """
        Sets the expiration time for a session in Redis.
        
        :param chat_session_id: The unique identifier for the session
        :param expiry: The expiry datetime
        """
        try:
            ttl_seconds = int((expiry - datetime.now()).total_seconds())
            if ttl_seconds < 0:
                print(f"Warning: Expiry time is in the past, setting TTL to 0")
                ttl_seconds = 0
            print(f"Setting expiry for session {chat_session_id}: TTL seconds = {ttl_seconds}")
            self.client.expire(chat_session_id, ttl_seconds)
        except redis.RedisError as e:
            print(f"Error setting session expiry: {str(e)}")

    def is_connected(self) -> bool:
        """
        Checks if the Redis server is connected.
        
        :return: True if connected, False otherwise
        """
        try:
            return self.client.ping()
        except redis.ConnectionError as e:
            print(f"Redis connection error: {str(e)}")
            return False
