from flask import Flask, jsonify

import pandas as pd
from src.dbService import esService
from src.constant import constant
from src.util import agencyIdRetriver
import json
from flask import current_app as app


def getResponse(startDate, endDate):
    df = getData(startDate, endDate)
    app.logger.info(f'for request: start-date-{startDate}, end-date-{endDate} data from es: \n{df}')
    formatedDf = formatData(df)
    app.logger.info(f'for request: start-date-{startDate}, end-date-{endDate} formated data:\n{formatedDf}')
    return makeResponse(formatedDf)

def makeResponse(df):
    print('final table: \n', df)
    agencyReportdict = {
        'data' : {
            'records' : [],
            'numberOfRecords' : 0
        },
        'error' : None
    }
    # agencyReportdict['requestSummary'] = []
    # agencyReportdict['data'] = []
    if(not df.empty):
        
        jsonResult = df.to_json(orient='table')
        agencyReportdict['data']['records'] = json.loads(jsonResult)['data']
        agencyReportdict['data']['numberOfRecords'] = len(agencyReportdict['data']['records'])
    return agencyReportdict

def getData(startDate, endDate):
    esQuery = buildQuery(startDate, endDate)
    esData = esService.search(index='search-summary-log', body=esQuery)
    df = pd.json_normalize(esData)
    return df




def formatData(df):
    print("search summary dataframe empty: ", df,df.empty)
    agencyReportdict = {}
    
    if (not df.empty):
        df = df[['_source.agency_id', '_source.user_id', '_source.request_type', '_source.search_summary_uuid']]
        df.columns = ['agency', 'user', 'request_type', 'search_summary_uuid']
        df['agency'] = df['agency'].apply(lambda agencyId: agencyIdRetriver.getAgencyId(agencyId))
        df.drop_duplicates(subset="search_summary_uuid", inplace=True)
        agencyWiseReport = df[['agency', 'request_type']].pivot_table(
            index='agency', columns='request_type', aggfunc=len, fill_value=0)

        
        agencyWiseReport = agencyWiseReport.reindex(agencyWiseReport.columns.union(constant.TaskTypes, sort=False), axis=1, fill_value=0)
        agencyWiseReport['TOTAL'] = agencyWiseReport.sum(axis=1)
        print("Agency wise summary report table: \n",agencyWiseReport)

        return agencyWiseReport


    return df


def buildQuery(startDate, endDate):
    query =  {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "searched_at": {
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
            'agency_id', 'user_id', 'request_type', 'search_summary_uuid'
        ]

    }

    app.logger.info(f'query for es: {query}')

    return query

