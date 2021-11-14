
import json
from flask import current_app as app
def subscribeToRedis(channels): 
    app.logger.info(f"In redis subscribe service || channels :{channels}")
    pubsub = app.redis_client.pubsub()
    try:
        redisResponse = pubsub.subscribe(channels)
        
    except Exception as e:
        app.logger.exception("Redis subscribe Failed")

    return pubsub


def listenToRedisChannel(channels, listener):
    data = []
    for message in listener.listen():
        app.logger.info(f"redis channel response:  {message}")

        if message.get("type") == "message":
            # app.logger.info("redis channel response:   "+str(message))
            # app.logger.info("Data from backend publisher (redis channels): "+message.get("data"))
            data.append(message.get("data"))
            return message.get("data")
    return data
            

