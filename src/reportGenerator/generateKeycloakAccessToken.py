import requests
import json
from flask import current_app as app



def getAccessToken():
    
    url = getUrl()
    headers = getHeader()
    data = getRequestBody()
    res = requests.post(url=url, data=data, headers=headers , verify=False)
    responseData =  res.json()
    app.logger.info(f'{responseData}')
    return responseData['access_token']  


def getUrl():
    subUrl = '/auth/realms/master/protocol/openid-connect/token'
    host = app.config['KEYCLOAK_HOST']
    url = host+subUrl
    app.logger.info('key cloak access token url: '+ url)
    return url


def getHeader():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return headers

def getRequestBody():
    data = {
        "client_id": "admin-cli",
        "username": app.config['KEYCLOAK_USERNAME'],
        "password": app.config['KEYCLOAK_PASSWORD'],
        "grant_type": "password"
    }

    return data

    