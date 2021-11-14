import pandas as pd
import numpy as np
import json
from datetime import datetime
from src.dbConfig import dbConfig
from src.constant import constant
from src.dbService import esService
from flask import current_app as app


def getResponse(body):
    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]
    df = getData(body)
    app.logger.info(f'df from es for request: {body} \n{df} ')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for request: {body} \n{df} ')
    return makeResponse(formatedDf)

def makeResponse(df):
    msisdnWithTimeRecords =  json.loads(df.to_json(orient = "records"))
    dataSize = len(msisdnWithTimeRecords)
    imeiWithTime = {
        "msisdnWithTime" : msisdnWithTimeRecords,
        "numberofRecords" : dataSize
    }

    return imeiWithTime

def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search(index = 'cdr', body = esQuery)
    df = pd.json_normalize(esData)
    return df


def formatData(df):
    if (not df.empty):
        df = df[['_source.imei_number', '_source.party_a',
                           '_source.event_time', '_source.call_duration']]
        df.replace("", np.nan, inplace=True)
        df.dropna(inplace=True)
        df['date_time'] = pd.to_datetime(
            df['_source.event_time'], format='%Y%m%d%H%M%S')
        df['subgroup'] = (df['_source.imei_number']
                               != df['_source.imei_number'].shift(1)).cumsum()

        app.logger.info(f'df after consecutive sub group: \n {df}')

        grpbySubgrp = df.groupby('subgroup')

        newDataframe = pd.DataFrame({'msisdn': grpbySubgrp['_source.party_a'].first(),
                                      'imei': grpbySubgrp['_source.imei_number'].first(),
                                      'lastCdrTime': grpbySubgrp.date_time.first(),
                                      'firstCdrTime': grpbySubgrp.date_time.last(),
                                      'cdrCount': grpbySubgrp.size(),
                                      'totalCallDurationS': grpbySubgrp['_source.call_duration'].sum()})

        
        newDataframe.loc[newDataframe['lastCdrTime'] == newDataframe['firstCdrTime'],
                          'lastCdrTime'] = newDataframe['firstCdrTime'] + pd.to_timedelta(newDataframe['totalCallDurationS'], unit='s')
        
        return newDataframe
    return pd.DataFrame([])




def buildQuery(body):
    
    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime("%Y%m%d%H%M%S") if 'startDate'  in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime("%Y%m%d%H%M%S") if 'endDate' in body else None

    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]

    esQuery = {
        "sort": [
            # {
            #     selectionCriteria+".keyword": "desc"
            # },
            {
                "event_time.keyword": "desc"
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            selectionCriteria: body['searchValue']
                        }
                    },
                    {
                        "range": {
                            "event_time": {
                                "gte": startDate,
                                "lte": endDate
                            }
                        }
                    }
                ],
                "must_not": [],
                "should": []
            }
        },
        "_source": [
            "party_a",
            "event_time",
            "imei_number",
            "call_duration",
            
        ]
    }

    return esQuery
