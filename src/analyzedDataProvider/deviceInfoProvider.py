import pandas as pd
import json
from src.constant import constant
from src.dbService import esService
from datetime import datetime
from flask import current_app as app
from src.util import msisdnPrefix
import numpy as np

def getResponse(body):
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f'data from es for request : {body} \n{df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for request : {body} \n{formatedDf}')
    return makeResponse(formatedDf)

def makeResponse(df):
    # deviceInfo =  json.loads(df.to_json(orient = "records"))
    # dataSize = len(deviceInfo)
    data = {
        # "deviceInfo" : deviceInfo,
        "msisdns": list(df.msisdn.unique()) if 'msisdn' in df.columns else [],
        "imeiNumbers": list(df.imeiNumber.unique()) if 'imeiNumber' in df.columns else [],
        "imsiNumbers": list(df.imsiNumber.unique()) if 'imsiNumber' in df.columns else [],
        # "numberofRecords" : dataSize
    }

    return data

def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search(index = 'cdr', body = esQuery)
    df = pd.json_normalize(esData)
    return df


def formatData(df):
    if (not df.empty):
        df = df[['_source.imei_number', '_source.imsi', '_source.party_a']]
        df.drop_duplicates(subset=['_source.imei_number', '_source.imsi', '_source.party_a'], inplace=True)
        df.rename(columns={
            '_source.imei_number': 'imeiNumber',
            '_source.imsi': 'imsiNumber',
            '_source.party_a': 'msisdn'
        }, inplace=True)

        return df
            
        
    return pd.DataFrame([])



def buildQuery(body):

    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]

    esQuery = {
        # "aggs": {
        #     "keys": {
        #         "terms": {
        #             "script": "[doc['_source.party_a'].value, doc['_source.imei_number'].value]"
                    
        #         }
        #     }
        # },
        "sort": [
            {
                "event_time.keyword": "desc"
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            selectionCriteria: body['searchValue']
                        }
                    }
                ]
            }
        },
        "_source": [
            "imei_number",
            "imsi",
            "party_a"
        ]
    }

    return esQuery
