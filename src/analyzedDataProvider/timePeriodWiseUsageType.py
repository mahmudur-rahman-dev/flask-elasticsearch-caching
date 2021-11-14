import pandas as pd
from src.dbConfig import dbConfig
from src.constant import constant
from datetime import datetime
from src.dbService import esService
from src.constant.timePeriods import TimePeriods 
from flask import current_app as app
from src.util import msisdnPrefix

def getResponse(body):
    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]
    # body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
    #     i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']
    
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']

    df = getData(body)
    app.logger.info(f'data from es for request: {body} \n {df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for request: {body} \n {formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(df):
    usageTypeTimePeriod = dict()
    for value in constant.timePeriods.values():
        usageTypeTimePeriod[constant.timePeriodsIncc[value]] = {
                 "timePeriod" : getTimePeriodefinition(value),
                 "records" : [],
                 "numberofRecords" : 0
        }

        if(len(df) > 0):
            usageTypeTimePeriod[constant.timePeriodsIncc[value]] = {
                "records" : formatGroupData(df.get_group(value)).to_dict(orient="records")  if value in df.groups else []
            }
            usageTypeTimePeriod[constant.timePeriodsIncc[value]]["numberofRecords"] =  len(usageTypeTimePeriod[constant.timePeriodsIncc[value]]["records"]) 

    return usageTypeTimePeriod

def formatGroupData(df):
    cdrSum = df.groupby(['partyB','usageType'])['usageType'].count().unstack().fillna(0)
    cdrSum.reset_index(inplace = True)
    usageTypeCols = ['MOC','MTC','SMSMO', 'SMSMT']
    formatedGrpDf = cdrSum.reindex(cdrSum.columns.union(usageTypeCols, sort=False), axis=1, fill_value=0.0)         
    return formatedGrpDf
 
        
def getTimePeriodefinition(periodName):
    enumValue = TimePeriods[periodName]
    return enumValue.value



def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)
    return df


def formatData(df):

    if (not df.empty):
        df = df[['_source.party_a','_source.party_b','_source.event_time','_source.usage_type']]
        df.columns = ['partyA','partyB', 'eventTime','usageType']
        
        df['dateTime'] = pd.to_datetime(df['eventTime'], format='%Y%m%d%H%M%S')
        df['period'] = (df['dateTime'].dt.hour % 24 + 4) // 4
        df['period'].replace(constant.timePeriods, inplace=True)
        
        app.logger.info(f'formted df with time period: \n{df}')
        
        grpByPeriod = df.groupby(['period'])
        
        return grpByPeriod
        
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
            "party_b",
            "event_time",
            "usage_type"
        ]
    }

    app.logger.info(f'query for request-body {body}: {esQuery}')

    return esQuery
