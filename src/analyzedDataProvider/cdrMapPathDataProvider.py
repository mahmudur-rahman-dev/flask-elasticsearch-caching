import pandas as pd
import json
from src.constant import constant
from datetime import datetime
from src.dbService import esService
from src.constant.timePeriods import TimePeriods
from flask import current_app as app
from src.util import msisdnPrefix

def getResponse(body):
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f'data from es for request: {body} \n {df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated dataframe for request: {body}: \n {formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(df):

    response = {
        'records' : df.to_dict(orient='records'),
        'numberOfRecords' : len(df)
    }

    return response




def formatData(df):

    if (not df.empty):
        df = df[['_source.party_a', '_source.party_b', '_source.event_time', '_source.usage_type',
                 '_source.bts.latitude', '_source.bts.longitude', '_source.bts.address', '_source.lac_start_a',
                 '_source.ci_start_a']]
        df.columns = ['partyA','partyB', 'eventTime', 'usageType','btsLatitude', 'btsLongitude', 'btsAddress', 'lacId', 'cellId']
        df = df.dropna(subset=['btsLatitude', 'btsLongitude', 'eventTime'])
        df['eventTime'] = pd.to_datetime(df['eventTime'], format='%Y%m%d%H%M%S').astype('int64')//1e9
        # df['eventTime'] = pd.to_datetime(df['eventTime'], format='%Y%m%d%H%M%S')
        app.logger.info(f'{df}')
        return df

    return pd.DataFrame([])


def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)
    return df


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime(
        "%Y%m%d%H%M%S") if 'startDate' in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime(
        "%Y%m%d%H%M%S") if 'endDate' in body else None

    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]


    esQuery = {
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
            "party_b",
            "event_time",
            "usage_type",
            "bts.latitude",
            "bts.longitude",
            "bts.address",
            "lac_start_a",
            "ci_start_a"
        
        ]
    }

    return esQuery
