from redisManager.redisManager import RedisManager

redis_manager=RedisManager()

redis_manager.is_connected()

if __name__=="main":
    redis_manager.set_message("session_1", {"role": "user", "content": "Hello, assistant!"})

# Retrieve messages for the session
    messages = redis_manager.get_messages("session_1")
    print(messages)