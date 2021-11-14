import pandas as pd
import json
from src.constant import constant
from src.dbService import esService
from datetime import datetime
from flask import current_app as app
from src.util import msisdnPrefix
import numpy as np

def getResponse(body):
    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]
    # body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(i) for i in body['searchValues']]
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f'data from es for request : {body} \n{df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for request : {body} \n{formatedDf}')
    return makeResponse(formatedDf)

def makeResponse(df):
    imeiWithTimeRecords =  json.loads(df.to_json(orient = "records"))
    dataSize = len(imeiWithTimeRecords)
    imeiWithTime = {
        "imeiWithTime" : imeiWithTimeRecords,
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
        df = df[['_source.party_a', '_source.imei_number', '_source.event_time', '_source.call_duration']]
            
        app.logger.info(f'dataframe for imei used with time requested by msisdn: \n{df}')
        df = df.replace("", np.nan).dropna()
        app.logger.info(f'nan value dropped from dataframe for imei used with time requested by msisdn: \n{df}')
        
        df['date_time'] = pd.to_datetime(
            df['_source.event_time'], format='%Y%m%d%H%M%S')
        df['subgroup'] = (df['_source.imei_number'] != df['_source.imei_number'].shift(1)).cumsum()

        app.logger.info(f'after adding subgrp"\n{df}')

        grpBySubgrp = df.groupby('subgroup')
        
        imeiTimeWiseDf = pd.DataFrame({
            'msisdn' : grpBySubgrp['_source.party_a'].first(),
            'imeiNumber': grpBySubgrp['_source.imei_number'].first(),
            'lastCdrTime': grpBySubgrp.date_time.first(),
            'firstCdrTime': grpBySubgrp.date_time.last(),
            'cdrCount': grpBySubgrp.size(),
            'totalCallDurationS': grpBySubgrp['_source.call_duration'].sum()})

        imeiTimeWiseDf.loc[imeiTimeWiseDf['lastCdrTime'] == imeiTimeWiseDf['firstCdrTime'],
            'lastCdrTime'] = imeiTimeWiseDf['firstCdrTime'] + pd.to_timedelta(imeiTimeWiseDf['totalCallDurationS'], unit='s')

        return imeiTimeWiseDf
        
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
            "imei_number",
            "event_time",
            "call_duration"
        ]
    }

    return esQuery
