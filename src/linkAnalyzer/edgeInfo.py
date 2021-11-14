import pandas as pd
from src.dbService import esService
from datetime import datetime
from flask import current_app as app
import json
from src.util import msisdnPrefix


def getResponse(body):
    # body['partyA'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA']) if body['searchCriteria'] == 'MSISDN' else body['partyA']
    df = getData(body)
    app.logger.info(f'df from es for request: {body}\n{df}')
    formatedDf = formatData(df, body)
    app.logger.info(f'formated df for request: {body}\n{formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(df):
    response = {
        "records": json.loads(df.to_json(orient="records"))
    }
    response['numberOfRecords'] = len(response['records'])

    return {'data': response, 'error': None}


def formatData(df, body):
    if(not df.empty):
        df = df[['_source.party_a','_source.party_b', '_source.usage_type',
                 '_source.event_time', '_source.call_duration']]
        df.columns = ['partyA','partyB', 'usageType', 'eventTime', 'duration']
        df.drop_duplicates(subset=['partyA', 'partyB', 'eventTime'], inplace=True)
        app.logger.info(f'df after dropping duplicates:\n{df}')

        df['startTime'] = pd.to_datetime(
            df['eventTime'], format='%Y%m%d%H%M%S')
        df['durationMS'] = pd.to_timedelta(df['duration'], unit='s')
        df['endTime'] = df['startTime'] + df['durationMS']
        
        if(msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA']) in df.partyA.values):
            df = df[(df['partyA'] == msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA'])) & (df['usageType'] == 'MOC')]
        elif(body['partyA'] in df.partyB.values) or (msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA']) in df.partyB.values):
            df = df[((df['partyB'] == body['partyA']) | (df['partyB']==msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA']))) & (df['usageType'] == 'MTC')]
        return df
    return df


def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search(index='cdr', body=esQuery)
    df = pd.json_normalize(esData)
    return df


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime(
        "%Y%m%d%H%M%S") if 'startDate' in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime(
        "%Y%m%d%H%M%S") if 'endDate' in body else None

    esQuery = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "party_a": [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA']),
                                        msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyB'])]
                        }
                    },
                    {
                        "terms": {
                            "party_b": [body['partyA'], msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyA']),
                                        body['partyB'], msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['partyB'])]
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
            "usage_type",
            "event_time",
            "call_duration"
        ]


      
    }

    app.logger.info(f'query for request-body {body}: {esQuery}')

    return esQuery
