import requests
import json
from flask import current_app as app



def getUserInfo(userId, accessToken):
    print("ACCESS token: ", accessToken)  
    url = getUrl(userId)
    headers = getHeader(accessToken)
    res = requests.get(url=url, headers = headers, verify=False)
    responseData = res.json()
    return responseData

def getUrl(userId):

    subUrl = getSubUrl()+userId
    host = app.config['KEYCLOAK_HOST']
    url = host+subUrl
    app.logger.info('key cloak host: '+ host)
    return url


def getSubUrl():
    subUrlForUserInfo = '/auth/admin/realms/'+ app.config['KEYCLOAK_REALM']+'/users/'
    subUrlForUserPermission = '/auth/realms/Dip/protocol/openid-connect/userinfo'
    return subUrlForUserInfo

def getHeader(accessToken):
    headers = {
        'Authorization' : "Bearer " + accessToken
    }

    return headers