from flask import current_app
import json
from flask import current_app as app
from src.constant.constant import getSearchedWith
def publishToRedis(body,response): 
    app.logger.info(f"In redis publish service || request type:{response['type']} || channels :{body['channels']}")
    for channel in body['channels']:
        try:
            response["publishedChannelName"]=channel
            response["searchedWith"]= getSearchedWith(body,response['type'])
            responseString = json.dumps(json.dumps(response,ensure_ascii=False),ensure_ascii=False)
            redisPublishResponse=current_app.redis_client.publish(channel,responseString)
            app.logger.info(f"Published to Redis Channel:{channel} || RequestType: {response['type']} || Redis Published Result:{redisPublishResponse}")
        except Exception as e:
            app.logger.exception("Redis publish Fail")
    
    return response

