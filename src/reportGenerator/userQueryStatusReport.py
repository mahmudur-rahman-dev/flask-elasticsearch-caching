from flask import Flask, jsonify
import pandas as pd
from src.dbService import esService
from src.constant import constant
from flask import current_app as app
from . import generateKeycloakAccessToken
from . import userInfoKeyCloak

taskTypesToSourceDB = {
    'DRIVINGLICENSE' : 'Driving-license',
    'BIRTHREGISTRATION' : 'Birth-registration',
    'NID' : 'NID',
    'PASSPORT' : 'Passport',
    'VEHICLEREGISTRATION': 'Vehicle-registration'
}

def getResponse(userId, startTime, endTime):
    df = getData(userId, startTime, endTime)
    app.logger.info(f'df for user: {userId} from es after search {df}')
    formatedDf = formatData(df, userId)
    app.logger.info(f'formated df for user : {userId} \n {formatedDf}')
    return makeResponse(formatedDf, userId)


def makeResponse(df, userId):
   
    response = {}
    app.logger.info('size of the dataframe: {0}'.format(len(df)))
    response['records'] =  df.to_dict(orient = "records")
    response['numberOfRecords'] = len(response['records'])
    
    return {"data": response, "error": None}



def formatData(df, userId):

    if(not df.empty):

        df.rename(columns={
            '_source.request_type': 'requestType',
            '_source.data_retrieval_status': 'status',
            '_source.searched_value.operator' : 'entity',
            '_source.user_id' : 'user'
        }, inplace=True)
      
        df = df[['requestType','status','entity','user']]
        df['entity'] = df['entity'].fillna(df['requestType'])
        df['entity'].replace(taskTypesToSourceDB, inplace=True)

        grpbyDf = df.groupby(['requestType','entity', 'status'])['status'].count().unstack().fillna(0).reset_index()

        if 'FAILURE' not in grpbyDf.columns:
            grpbyDf['FAILURE']=0

        grpbyDf.rename(columns={
            'SUCCESS': 'success',
            'FAILURE': 'failure'
        }, inplace=True)

        grpbyDf['total'] = grpbyDf['success'] + grpbyDf['failure']

        return grpbyDf

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
            'data_retrieval_status', 'request_type', 'searched_value.operator' , 'user_id'
        ]

    }
    
    app.logger.info(f'query for es: {query}')

    return query
