import pandas as pd
from elasticsearch import Elasticsearch

from datetime import datetime
from src.dbConfig import dbConfig
from src.constant import constant
from src.dbService import esService
from src.util import msisdnPrefix
from flask import current_app as app


def getResponse(body):
    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]
    # body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
    #     i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']
    
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df =  getData(body)
    app.logger.info(f'data from es for request {body} \n{df}')
    formatedDf = formatData(df)
    app.logger.info(f'processed df of usage-type for request: {body} \n{formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(df):
    
    usageTypeSummary = df.to_dict(orient="records")
    dataSize = len(usageTypeSummary)

    usageTypeSummaryData = {
        "usageTypeSummary" : usageTypeSummary,
        "numberofRecords" : dataSize
    }

    return usageTypeSummaryData

def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)
    return df

def formatData(df):
    app.logger.info(f'df of es data: \n{df}')
    if (not df.empty):
        df = df[['_source.party_a', '_source.party_b','_source.usage_type']]
        df.columns = ['partyA',  'partyB', 'usageType']
        grpBydf = df.groupby(['partyB','usageType'])['usageType'].count().unstack().fillna(0)
        
        usageTypeSummaryDf =  grpBydf.reset_index()

        app.logger.info(f'df after group by: \n {usageTypeSummaryDf}')
        usageTypeCols = ['MOC','MTC','SMSMO', 'SMSMT']
        usageTypeSummaryDf = usageTypeSummaryDf.reindex(usageTypeSummaryDf.columns.union(usageTypeCols, sort=False), axis=1, fill_value=0)
            
        return usageTypeSummaryDf

    return pd.DataFrame([])


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime("%Y%m%d%H%M%S") if 'startDate'  in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime("%Y%m%d%H%M%S") if 'endDate' in body else None
    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]

    esQuery = {
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
            "party_a", "party_b", "usage_type"
        ]


    }

    return esQuery