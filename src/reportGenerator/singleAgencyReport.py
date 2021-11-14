from flask import Flask, jsonify
from datetime import datetime
import pandas as pd
from src.dbService import esService
from . import generateKeycloakAccessToken
from . import userInfoKeyCloak
from flask import current_app as app
from src.util import agencyIdRetriver


def getResponse(agencyId, startTime, endTime):
    df = getData(agencyId=agencyId, startTime=startTime, endTime=endTime)
    app.logger.info(
        f'df from es for request {agencyId}, {startTime}, {endTime}\n {df}')
    formatedDf = formatData(df)
    app.logger.info(
        f'fromated df for request {agencyId}, {startTime}, {endTime}\n {formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(groupbyDf):

    responseRecords = {
        "records": []
    }
    app.logger.info('size of the dataframe: ')
    if(len(groupbyDf) is not 0):
        accessToken = generateKeycloakAccessToken.getAccessToken()
        app.logger.info("Access token from keycloak: " + accessToken)

        print("size of dataframe: ", )
        for user in groupbyDf.groups:
            responseRecords["records"].append(
                makeGroupResponse(groupbyDf, user, accessToken))

    responseRecords['numberOfRecords'] = len(responseRecords['records'])

    return {"data": responseRecords, "error": None}


def makeGroupResponse(groupbyDf, userId, accessToken):
    df = groupbyDf.get_group(userId)
    userInfo = getUserInfo(userId, accessToken)
    name = userInfo['name']
    userName = userInfo['userName']

    print("User name : ", userName)
    totalQuery = len(df)
    userResponse = {
        "user": {
            "id": userId,
            "name": name,
            "userName": userName
        },
        "totalQuery": totalQuery,
        "totalSuccessfullQuery": len(df[df['queryStatus'] == 'SUCCESS']),
        "totalFailedQuery": len(df[df['queryStatus'] == 'FAILURE'])
    }
    return userResponse


def getUserInfo(userId, accessToken):

    userInfo = userInfoKeyCloak.getUserInfo(
        userId=userId, accessToken=accessToken)
    user = {
        'name': '',
        'userName': ''
    }
    if 'error' not in userInfo:
        app.logger.info('user :' + userId + 'user info: {0}'.format(userInfo))
        if('firstName' in userInfo):
            user['name'] = f"{userInfo['firstName']} "
        if('lastName' in userInfo):
            user['name'] = f"{user['name']}{userInfo['lastName']}"
        if('userName' in userInfo):
            user['userName'] = userInfo['username']

    return user


def formatData(df):

    if(not df.empty):
        # df = df[['_source.agency_id', '_source.user_id',
        #          '_source.data_retrieval_status', '_source.search_summary_uuid']]
        
        #ordering requestTypes as success and failure to keep only success requests from same request_uuid        
        app.logger.info(f'df before setting status as category and sorting :\n{df}')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].astype('category')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].cat.set_categories(['SUCCESS', 'FAILURE'], ordered=True)
        app.logger.info(f'df after setting status as category and sorting :\n{df}')
        df.sort_values(['_source.search_summary_uuid', '_source.data_retrieval_status'], inplace=True)
        df.drop_duplicates(subset="_source.search_summary_uuid", inplace=True)

        df = df[['_source.agency_id', '_source.user_id',
                 '_source.data_retrieval_status']]
        df.columns = ['agency', 'userId', 'queryStatus']
        df['agency'] = df['agency'].apply(
            lambda agencyId: agencyIdRetriver.getAgencyId(agencyId))

        print(df)
        return df.groupby('userId')

    return df


def getData(agencyId, startTime, endTime):
    esQuery = buildQuery(agencyId,  startTime, endTime)
    esData = esService.search('search-summary-log', esQuery)
    df = pd.json_normalize(esData)
    return df


def buildQuery(agency_id,  startTime, endTime):
    query = {
        "query": {

            "bool": {
                "must": [
                    {
                        "wildcard": {
                            "agency_id.keyword": "/"+agency_id+"*"
                        }
                    },

                    {
                        "range": {
                            "searched_at": {
                                "gte": startTime,
                                "lte": endTime
                            }
                        }
                    }
                ],
                "must_not": [],
                "should": []
            }

        },

        "_source": [
            'agency_id', 'user_id', 'data_retrieval_status', 'search_summary_uuid'
        ]

    }
    # query["query"]["regexp"]={
    #   "agency_id": {
    #     "value": "*"+agency_id+"*",
    #     "flags": "ALL",
    #     "case_insensitive": True
    #   }
    # }

    app.logger.info(f'built query for es: {query}')

    return query
