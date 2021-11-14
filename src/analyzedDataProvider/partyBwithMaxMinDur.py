import pandas as pd
from datetime import datetime
from src.constant import constant
from src.dbService import esService
from flask import current_app as app
from src.util import msisdnPrefix
numberOfmsisdns = 5

def getResponse(body):
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f'data from es for request : {body} \n{df}')
    maxDurationDataUT = formatDataByUsagetype(df, "max")
    minDurationDataUT = formatDataByUsagetype(df, "min")
    app.logger.info(
        f'formated df for max duration Bparties\n {maxDurationDataUT}')
    app.logger.info(
        f'formated df for min duration Bparties\n {minDurationDataUT}')

    maxDurationBparty = formatDataforMaxMinDuration(df, "max")
    minDurationBparty = formatDataforMaxMinDuration(df, "min")
    app.logger.info(
        f'formated df for usage-type wise max duration Bparties\n{maxDurationDataUT}')
    app.logger.info(
        f'formated df for usage-type wise min duration Bparties\n{minDurationBparty}')

    return makeResponse(maxDurationBparty, minDurationBparty, maxDurationDataUT, minDurationDataUT)


def makeResponse(maxDurationBparty, minDurationBparty, usageTypeWiseMax, usageTypeWiseMin):

    responseData = {
        'partyBWithMaxDuration': {'records': [], 'numberofRecords': 0},
        'partyBWithMinDuration': {'records': [], 'numberofRecords': 0},
        'moc': {'maxDuration': {'records': [], 'numberofRecords': 0},
                'minDuration': {'records': [], 'numberofRecords': 0}},
        'mtc': {'maxDuration': {'records': [], 'numberofRecords': 0},
                'minDuration': {'records': [], 'numberofRecords': 0}}
    }

    if(len(maxDurationBparty) > 0):
        responseData['partyBWithMaxDuration']['records'] = maxDurationBparty.to_dict(
            orient='records')
        responseData['partyBWithMaxDuration']['numberofRecords'] = len(
            responseData['partyBWithMaxDuration']['records'])

    if(len(minDurationBparty) > 0):
        responseData['partyBWithMinDuration']['records'] = minDurationBparty.to_dict(
            orient='records')
        responseData['partyBWithMinDuration']['numberofRecords'] = len(
            responseData['partyBWithMinDuration']['records'])

    if(len(usageTypeWiseMax) > 0):
        print('type of dataframe in max-usage-type:     \n',type(usageTypeWiseMax) )
        responseData['moc']['maxDuration']['records'] = formatEachGrp(usageTypeWiseMax.get_group(
            'MOC'), 'max').to_dict(orient='records') if "MOC" in usageTypeWiseMax.groups else []
        responseData['moc']['maxDuration']['numberofRecords'] = len(
            responseData['moc']['maxDuration']['records'])
        responseData['mtc']['maxDuration']['records'] = formatEachGrp(usageTypeWiseMax.get_group(
            'MTC'), 'max').to_dict(orient='records') if "MTC" in usageTypeWiseMax.groups else []
        responseData['mtc']['maxDuration']['numberofRecords'] = len(
            responseData['mtc']['maxDuration']['records'])

    if(len(usageTypeWiseMin) > 0):
        responseData['moc']['minDuration']['records'] = formatEachGrp(usageTypeWiseMin.get_group(
            'MOC'), 'min').to_dict(orient='records') if "MOC" in usageTypeWiseMin.groups else []
        responseData['moc']['minDuration']['numberofRecords'] = len(
            responseData['moc']['minDuration']['records'])
        responseData['mtc']['minDuration']['records'] = formatEachGrp(usageTypeWiseMin.get_group(
            'MTC'), 'min').to_dict(orient='records') if "MTC" in usageTypeWiseMin.groups else []
        responseData['mtc']['minDuration']['numberofRecords'] = len(
            responseData['mtc']['minDuration']['records'])

    return responseData


def formatEachGrp(df, max_or_min):
    if max_or_min=='max' :
        df = df.nlargest(numberOfmsisdns, 'callDuration')
    if max_or_min=='min':
        df = df.nsmallest(numberOfmsisdns, 'callDuration')

    df.drop(columns=['usageType'], inplace=True)
    return df


def formatDataByUsagetype(df, max_or_min):

    if (not df.empty):
        df = df[['_source.party_a', '_source.party_b',
                 '_source.usage_type', '_source.call_duration']]
        df.columns = ['partyA', 'partyB', 'usageType', 'callDuration']

        aggrUsageType = df.groupby(['usageType'])

        # app.logger.info(f'df after aggregation: \n{aggrUsageType}')

        # aggrUsageType.rename(
        #     columns={"usageType": "usageTypeCount"}, inplace=True)
        # aggrDf = aggrUsageType.reset_index()

        # app.logger.info(f'df after aggregation reset: \n{aggrDf}')

        # maxminDurationRows = aggrDf.groupby(['usageType'])['callDuration'].transform(
        #     max_or_min) == aggrDf['callDuration']
        # maxminDurationDf = aggrDf[maxminDurationRows]
        # grpByUsagetypeDf = maxminDurationDf.groupby('usageType')
        # grpByUsagetypeDf = aggrDf.groupby('usageType')

        return aggrUsageType
        # print(aggrUsageType.index)
        # return aggrUsageType
    return pd.DataFrame([])


def formatDataforMaxMinDuration(df, max_or_min):

    if (not df.empty):
        df = df[['_source.party_a', '_source.party_b',
                 '_source.usage_type', '_source.call_duration']]
        df.columns = ['partyA', 'partyB', 'usageType', 'callDuration']
        app.logger.info(f'df for MOC and MTC: \n {df}')

        if(max_or_min is "max"):
            return df.nlargest(numberOfmsisdns, 'callDuration')
            
        if(max_or_min is "min"):
            return df.nsmallest(numberOfmsisdns, 'callDuration')
            

        return aggrByPartyB

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
        '_source' : ['party_a', 'party_b', 'usage_type', 'call_duration']


    }

    return esQuery
