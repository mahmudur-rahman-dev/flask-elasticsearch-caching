from flask import Flask, jsonify
import pandas as pd
from src.dbService import esService
from src.constant import constant
from flask import current_app as app


def getResponse(userId,startDate, endDate):
    df = getData(userId,startDate,endDate)
    app.logger.info(f'df for user: {userId} from es after search {df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for user : {userId} \n {formatedDf}')
    return makeResponse(formatedDf)


def getData(userId,startTime,endTime):    
    esQuery = buildQuery(userId,startTime,endTime)
    esData = esService.search(index='search-summary-log',body= esQuery)
    df = pd.json_normalize(esData)
    app.logger.info("Dataframe of search summary data: {0}".format(esData))
    return df


def makeResponse(df):
    responseRecords = {}
    app.logger.info('size of the dataframe: {0}'.format(len(df)))
    responseRecords['records'] =  df.to_dict(orient = "records")
    responseRecords['numberOfRecords'] = len(responseRecords['records'])
    return {"data": responseRecords, "error": None}
            


def formatData(df):

    if(not df.empty):
        df = df[['_source.searched_at', '_source.request_type', '_source.search_summary_uuid']]
        df.drop_duplicates('_source.search_summary_uuid', inplace=True)
        df.rename(columns={
            '_source.searched_at': 'searchTime',
            '_source.request_type' : 'requestType',
        }, inplace=True)
        

        df['time'] =  pd.to_datetime(df['searchTime']).dt.strftime('%I %p')
        grpby = df.groupby(['time', 'requestType']).size().reset_index(name='count')
        app.logger.info(f'{df.dtypes}')
        return grpby

    return df
  


def buildQuery(userId,startTime,endTime):
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
        "_source" : [
                'searched_at', 'request_type', 'search_summary_uuid'
        ]

    }

    return query
