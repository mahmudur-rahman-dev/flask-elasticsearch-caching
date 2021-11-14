import pandas as pd
from src.dbService import esService
from src.analyzedDataProvider import cdrUsageTypeFre
from datetime import datetime
from flask import current_app as app
from src.util import msisdnPrefix

def getResponse(body):
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    formatedDf = formatData(df)
    return makeResponse(formatedDf, body)


def makeResponse(df, body):
    partyBinfo = cdrUsageTypeFre.getResponse(body=body)
    response = {}
    response['imeiNumbers'] = df['imeiNumber'].unique(
    ).tolist() if 'imeiNumber' in df else None
    response['imsiNumbers'] = df['imsiNumber'].unique(
    ).tolist() if 'imsiNumber' in df else None
    response['cdrSummary'] = {
        'numberOfRecords': partyBinfo['numberofRecords'],
        'records': partyBinfo['usageTypeSummary']
    }

    return {"data": response, "error": None}


def formatData(df):
    if(not df.empty):
        print(df)
        df = df[['_source.party_a', '_source.imei_number', '_source.imsi']]
        df.columns = ['partyA', 'imeiNumber', 'imsiNumber']
        return df
    return df


def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search(index='cdr', body=esQuery)
    app.logger.info(f"ES data for request {body}\n{esData}")
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
                        "match": {
                            "party_a": body['searchValue']
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
            "imsi"
        ]

    }

    app.logger.info(f'query for request-body {body}: {esQuery}')

    return esQuery
