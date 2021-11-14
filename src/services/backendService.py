import requests
from flask import current_app
def postToMno(body,uriPath):
    app = current_app
    url = app.config["ENQUERUER_URL"]+uriPath
    app.logger.info(f"Call made to backend URL:{url} || with Body:{body}")
    headers = {'Content-type': 'application/json'}
    try:
        return requests.post(url=url, json=body,headers=headers).json()
    except:
        app.logger.exception("Error occurred while posting to backend!")
    
