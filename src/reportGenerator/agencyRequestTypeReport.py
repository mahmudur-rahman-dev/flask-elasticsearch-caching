import pandas as pd
from src.dbService import esService
from src.constant import constant
from flask import current_app as app
from src.util import agencyIdRetriver
from . import generateKeycloakAccessToken
from . import userInfoKeyCloak

def getResponse(requestType, agencyId, startTime, endTime):
    df = getData(requestType, agencyId, startTime, endTime)
    app.logger.info(
        f'df from es data for request-type {requestType} and agency {agencyId} :  \n{df}')
    formatedDf = formatData(df, requestType)
    app.logger.info(
        f'formated df for request: {requestType} {agencyId} {startTime} {endTime} \n{formatedDf}')
    dfWithUser = getDfwithUserInfo(formatedDf)
    app.logger.info(
        f'for agency: {agencyId}, start-date: {startTime}, end-date: {endTime}, df with user info: \n{dfWithUser} ')
    return makeResponse(dfWithUser)


def makeResponse(df):
    response = {
        'records' : [],
        'numberOfRecords' : 0
    }
    if not df.empty:
        response['records'] = df.to_dict(orient='records')
        response['numberOfRecords'] = len(response['records'])
    return {'data': response, 'error' : None}


def getDfwithUserInfo(df):
    if(not df.empty):
        accessToken = generateKeycloakAccessToken.getAccessToken()
        df['user'] = df.apply(lambda row: getUserInfofromkeycloak(
            str(row.name), accessToken), axis=1)
        app.logger.info(f'dataframe with user {df}')

    return df


def getUserInfofromkeycloak(userId, accessToken):
    app.logger.info(
        f'access-token to get user info from key-cloak: {accessToken}')
    userInfo = userInfoKeyCloak.getUserInfo(
        userId=userId, accessToken=accessToken)

    user = {
        'id': userId,
        'name': '',
        'userName': ''
    }

    if 'error' not in userInfo:
        app.logger.info('user :' + userId + 'user info: {0}'.format(userInfo))
        user['name'] = f"{userInfo['firstName']} " if(
            'firstName' in userInfo) else ''
        user['name'] = f"{user['name']}{userInfo['lastName']}" if(
            'lastName' in userInfo) else ''
        user['userName'] = userInfo['username'] if(
            'userName' in userInfo) else ''

    app.logger.info(f'user-ID: {userId} , user-info: {userInfo}')

    return user



def formatData(df, requestType):
    if not df.empty:

        #ordering requestTypes as success and failure to keep only success requests from same request_uuid        
        app.logger.info(f'df before setting status as category and sorting :\n{df}')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].astype('category')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].cat.set_categories(['SUCCESS', 'FAILURE'], ordered=True)
        app.logger.info(f'df after setting status as category and sorting :\n{df}')
        df.sort_values(['_source.search_summary_uuid', '_source.data_retrieval_status'], inplace=True)
        df.drop_duplicates(subset="_source.search_summary_uuid", inplace=True)

        
        df['_source.searched_value.selectionCriteria'] = df['_source.searched_value.selectionCriteria'].apply(str)
        df['_source.searched_value.selectionCriteria'].replace(constant.searchCriteriaByID, inplace=True)
        
        # df = getColumnsForSearchValue(df, requestType)
        df.rename(columns={
            '_source.searched_at': 'searchTime',
            '_source.responded_at': 'responseTime',
            '_source.user_id': 'user',
            '_source.agency_id': 'agency',
            '_source.data_retrieval_status': 'status',
            '_source.searched_value.selectionCriteria' : 'identifierType',
            '_source.searched_value.searchedWith' : 'identifierValue'
        }, inplace=True)

        df['agency'] = df['agency'].apply(
            lambda agencyId: agencyIdRetriver.getAgencyId(agencyId))


        df = df[['searchTime', 'responseTime', 'status', 'user',
                 'agency', 'identifierType', 'identifierValue']]
        return df
    return df


# def getColumnsForSearchValue(df, requestType):
#     columns = constant.ColumnNameforSearchedValue[requestType]
#     changedColumns = list(
#         map(lambda x: '_source.searched_value.' + x, columns))
#     app.logger.info(
#         f'column name of searched value for requestType {changedColumns}')
#     df['identifierValue'] = df[changedColumns].apply(
#         lambda row: '-'.join(row.values.astype(str)), axis=1)
#     app.logger.info(f'changed df {df}')
#     return df


def getData(requestType, agencyId, startTime, endTime):
    esQuery = buildQuery(requestType, agencyId, startTime, endTime)
    esData = esService.search(index="search-summary-log", body=esQuery)
    df = pd.json_normalize(esData)
    return df


def buildQuery(requestType, agencyId, startTime, endTime):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "request_type": requestType.upper()
                        }
                    },
                    {                       
                        "wildcard": {
                            "agency_id.keyword": "/"+agencyId+"*"
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
            'agency_id', 'user_id', 'data_retrieval_status', 'searched_at', 'responded_at', 'request_type', 'searched_value.selectionCriteria' ,'searched_value.searchedWith', 'search_summary_uuid'
        ]

    }


    app.logger.info(f'query for es: {query}')


    return query
