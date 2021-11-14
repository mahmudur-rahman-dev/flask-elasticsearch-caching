import pandas as pd
from datetime import datetime
from src.constant import constant
from src.dbService import esService
from flask import current_app as app
from src.util import msisdnPrefix

def getResponse(body):
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f'data from es for request {body} \n{df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for request {body} \n{formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(df):
    companySms = {}
    companySms['companySms'] = df.to_dict(orient = "records")
    companySms['numberofRecords'] = len(companySms['companySms'])
    return companySms


def getData( body):
    esQuery = buildQuery(body)
    esData = esService.search('sms', esQuery)
    df = pd.json_normalize(esData)
    
    return df


def formatData(df):
    if (not df.empty):
        df = df[['_source.party_a', '_source.event_time', '_source.content']]
        df.columns = ['sender', 'eventTime', 'content']
        df['eventTime'] = pd.to_datetime(df['eventTime'], format='%Y%m%d%H%M%S')
        return df
    return df



def buildQuery(body):


    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime(
        "%Y%m%d%H%M%S") if 'startDate' in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime(
        "%Y%m%d%H%M%S") if 'endDate' in body else None

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
                            'party_b': body['searchValue']
                        }
                    },
                    {
                        "range": {
                            "event_time": {
                                "gte": startDate,
                                "lte": endDate
                            }
                        }
                    },
                    {
                        "regexp": {
                            "party_a": {
                                "value": "[a-zA-Z]+",
                                "flags": "ALL",
                                "case_insensitive": "true",
                                "rewrite": "constant_score"
                            }
                        }
                    }
                ]
            }
        },
        "_source": [
            "party_a",
            "event_time",
            "content"
        ]
    }
    return esQuery
