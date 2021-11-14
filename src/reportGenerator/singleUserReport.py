from flask import Flask, jsonify
import pandas as pd
from src.dbService import esService
from src.constant import constant
from flask import current_app as app
from . import generateKeycloakAccessToken
from . import userInfoKeyCloak

def getResponse(userId, startTime, endTime):
    df = getData(userId, startTime, endTime)
    app.logger.info(f'df for user: {userId} from es after search {df}')
    formatedDf = formatData(df, userId)
    app.logger.info(f'formated df for user : {userId} \n {formatedDf}')
    return makeResponse(formatedDf, userId)


def makeResponse(df, userId):
   
    response = {
        'cdr': {'records': [], 'numberOfRecords': 0},
        'esaf': {'records': [], 'numberOfRecords': 0},
        'sms': {'records': [], 'numberOfRecords': 0},
        'lrl': {'records': [], 'numberOfRecords': 0},
        'birthRegistration': {'records': [], 'numberOfRecords': 0},
        'vehicleRegistration': {'records': [], 'numberOfRecords': 0},
        'nid': {"records": [], 'numberOfRecords': 0},
        'drivingLicense': {'records': [], 'numberOfRecords': 0},
        'passport': {'records': [], 'numberOfRecords': 0}
    }
    # app.logger.info('size of the dataframe: {0}'.format(len(df)))
    # responseRecords['records'] =  df.to_dict(orient = "records")
    # responseRecords['numberOfRecords'] = len(responseRecords['records'])
    if(len(df) > 0):
        response["esaf"]["records"] = df.get_group('ESAF').to_dict(
            orient='records') if 'ESAF' in df.groups else []
        response["esaf"]["numberOfRecords"] = len(response['esaf']["records"])

        response["cdr"]["records"] = df.get_group('CDR').to_dict(
            orient='records') if 'CDR' in df.groups else []
        response["cdr"]["numberOfRecords"] = len(response['cdr']['records'])

        response["sms"]["records"] = df.get_group('SMS').to_dict(
            orient='records') if 'SMS' in df.groups else []
        response["sms"]["numberOfRecords"] = len(response['sms']['records'])

        response["lrl"]["records"] = df.get_group('LRL').to_dict(
            orient='records') if 'LRL' in df.groups else []
        response["lrl"]["numberOfRecords"] = len(response['lrl']['records'])

        response["birthRegistration"]["records"] = df.get_group('BIRTHREGISTRATION').to_dict(
            orient='records') if 'BIRTHREGISTRATION' in df.groups else []
        response["birthRegistration"]["numberOfRecords"] = len(
            response['birthRegistration']['records'])

        response["vehicleRegistration"]["records"] = df.get_group('VEHICLEREGISTRATION').to_dict(
            orient='records') if 'VEHICLEREGISTRATION' in df.groups else []
        response["vehicleRegistration"]["numberOfRecords"] = len(
            response['birthRegistration']["records"])

        response["nid"]["records"] = df.get_group('NID').to_dict(
            orient='records') if 'NID' in df.groups else []
        response["nid"]["numberOfRecords"] = len(response['nid']['records'])

        response["drivingLicense"]["records"] = df.get_group('DRIVINGLICENSE').to_dict(
            orient='records') if 'DRIVINGLICENSE' in df.groups else []
        response["drivingLicense"]["numberOfRecords"] = len(
            response['drivingLicense']["records"])

        response["passport"]["records"] = df.get_group('PASSPORT').to_dict(
            orient='records') if 'PASSPORT' in df.groups else []
        response["passport"]["numberOfRecords"] = len(
            response['passport']['records'])

    return {"data": response, "error": None}

def getUserInfo(userId):

    accessToken = generateKeycloakAccessToken.getAccessToken()
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




def formatData(df, userId):

    if(not df.empty):

        #ordering requestTypes as success and failure to keep only success requests from same request_uuid        
        app.logger.info(f'df before setting status as category and sorting :\n{df}')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].astype('category')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].cat.set_categories(['SUCCESS', 'FAILURE'], ordered=True)
        app.logger.info(f'df after setting status as category and sorting :\n{df}')
        df.sort_values(['_source.search_summary_uuid', '_source.data_retrieval_status'], inplace=True)
        df.drop_duplicates(subset="_source.search_summary_uuid", inplace=True)
        

        df['_source.searched_value.selectionCriteria'] = df['_source.searched_value.selectionCriteria'].apply(
            str)
                
        df['_source.start_date'] = df['_source.start_date'].fillna(-1)
        df['_source.end_date'] = df['_source.end_date'].fillna(-1)
        df['_source.start_date'] = df['_source.start_date']*1000
        df['_source.end_date'] = df['_source.end_date']*1000
        
        # df['_source.start_date'] = df['_source.start_date'].astype('int64').where(df['_source.start_date'].notnull())
        # df['_source.end_date'] = df['_source.end_date'].astype('int64')

        df['_source.searched_value.selectionCriteria'].replace(
            constant.searchCriteriaByID, inplace=True)
        df.rename(columns={
            '_source.searched_at': 'searchTime',
            '_source.responded_at': 'responseTime',
            '_source.data_retrieval_status': 'status',
            '_source.request_type': 'requestType',
            '_source.searched_value.selectionCriteria': 'identifierType',
            '_source.searched_value.searchedWith': 'identifierValue',
            '_source.start_date': 'startDate',
            '_source.end_date': 'endDate',
            '_source.user_id' : 'user',
            '_source.search_mode': 'searchContext'
            
        }, inplace=True)
        user = getUserInfo(userId)
        app.logger.info(f'user info for user-id {userId}: {user}')
        df['userName'] = user['name']      
        df = df[['searchTime', 'responseTime', 'status', 'requestType',
                 'identifierType', 'identifierValue','startDate', 'endDate', 'searchContext', 'userName']]

        return df.groupby('requestType')
    return df


def getData(userId, startTime, endTime):
    esQuery = buildQuery(userId, startTime, endTime)
    esData = esService.search(index='search-summary-log', body=esQuery)
    df = pd.json_normalize(esData)
    app.logger.info("Dataframe of search summary data: {0}".format(esData))
    return df


def buildQuery(userId, startTime, endTime):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "user_id.keyword": userId
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
            'data_retrieval_status', 'searched_at', 'responded_at', 'request_type', 'searched_value.selectionCriteria', 'searched_value.searchedWith', 'start_date', 'end_date', 'search_mode', 'user_id' , 'search_summary_uuid'
        ]

    }

    app.logger.info(f'query for es: {query}')

    return query
