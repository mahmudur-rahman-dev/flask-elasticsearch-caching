from src.reportGenerator import generateKeycloakAccessToken
from src.reportGenerator import userInfoKeyCloak

def getResponse(userId):
    accessToken = generateKeycloakAccessToken.getAccessToken()
    userInfo = userInfoKeyCloak.getUserInfo(userId=userId, accessToken=accessToken)
    return userInfo

def makeResponse(userInfo):
    respone = {
        'name' : userInfo['']
    }