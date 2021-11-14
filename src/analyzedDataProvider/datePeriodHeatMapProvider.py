import pandas as pd
import numpy as np
from datetime import datetime
from src.constant import constant
from src.dbService import esService
from flask import current_app as app
from src.util import msisdnPrefix

getValueColumn = {
    'cdr-count' : 'usageType',
    'total-duration' : 'callDuration'
}

def getResponse(body, generateBy):
    if 'searchValue' in body:
        body['searchValues'] = [body['searchValue']]
    body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
        i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']
    
    # body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f"data from es for most spending time for request: {body} \n{df}") 
    formatedDf =  formatData(df)
    heatMapDf = generateDataBy(formatedDf, generateBy)
    return makeResponse(heatMapDf)


def makeResponse(df):
    # response={}
    # response["dateTimePeriodData"]={
    #     "records" : df.to_dict(orient="records") if not df.empty else []
    # }
    response ={
        "records" : df.to_dict(orient="records") if not df.empty else []
    }
    response["numberofRecords"] = len(response["records"])
    app.logger.info(f'response: {response}')
    return response

    
def generateDataBy(df, generateBy):
    df.rename(columns={
        getValueColumn[generateBy] : 'value'
    }, inplace=True)

    app.logger.info(f'df for data of heatmap: \n{df}')

    return df


def formatData(df):

    if (not df.empty):
        df = df[['_source.party_a','_source.party_b', '_source.event_time', '_source.usage_type', '_source.call_duration']]
        df.columns = ['partyA','partyB', 'eventTime', 'usageType', 'callDuration']
        df.replace("", np.nan, inplace=True)
        df = df.dropna()

        df['dateTime'] = pd.to_datetime(
            df['eventTime'], format='%Y%m%d%H%M%S')
        df['date'] = df['dateTime'].dt.date
        df['period'] = (df['dateTime'].dt.hour % 24 + 4) // 4
        df['period'].replace(constant.timePeriods, inplace=True)
        app.logger.info(f'df after adding date and period columns: \n{df}')

        aggrDfBydatePeriod = df.groupby(['date', 'period']).agg({
                'usageType': 'size',
                'callDuration': 'sum'
            })

        app.logger.info(f'df after adding date and period columns: \n{aggrDfBydatePeriod}')
        
        return aggrDfBydatePeriod.reset_index()

    return pd.DataFrame([])




def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)
    app.logger.info(f'data from es for request :{body}\n {df}')
    return df


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime(
        "%Y%m%d%H%M%S") if 'startDate' in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime(
        "%Y%m%d%H%M%S") if 'endDate' in body else None
    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper(
    )]

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
        '_source' : ['party_a', 'party_b', 'event_time', 'usage_type', 'call_duration']


    }

    return esQuery
