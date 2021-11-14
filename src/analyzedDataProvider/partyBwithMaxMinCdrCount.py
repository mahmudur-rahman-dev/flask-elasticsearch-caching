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
    maxCountDataUT = formatDataByUsagetype(df, "max")
    minCountDataUT = formatDataByUsagetype(df, "min")
    app.logger.info(
        f'formated df for max duration Bparties\n {maxCountDataUT}')
    app.logger.info(
        f'formated df for min duration Bparties\n {minCountDataUT}')

    maxCountBparty = formatDataforMaxMinCount(df, "max")
    minCountBparty = formatDataforMaxMinCount(df, "min")
    app.logger.info(
        f'formated df for usage-type wise max duration Bparties\n{maxCountBparty}')
    app.logger.info(
        f'formated df for usage-type wise min duration Bparties\n{minCountBparty}')

    return makeResponse(maxCountBparty, minCountBparty, maxCountDataUT, minCountDataUT)


def makeResponse(maxCountBparty, minCountBparty, usageTypeWiseMax, usageTypeWiseMin):

    responseData = {
        'partyBWithMaxCount': {'records': [], 'numberofRecords': 0},
        'partyBWithMinCount': {'records': [], 'numberofRecords': 0},
        'moc': {'maxCount': {'records': [], 'numberofRecords': 0},
                'minCount': {'records': [], 'numberofRecords': 0}},
        'mtc': {'maxCount': {'records': [], 'numberofRecords': 0},
                'minCount': {'records': [], 'numberofRecords': 0}},
        'smsmo': {'maxCount': {'records': [], 'numberofRecords': 0},
                'minCount': {'records': [], 'numberofRecords': 0}},
        'smsmt': {'maxCount': {'records': [], 'numberofRecords': 0},
                'minCount': {'records': [], 'numberofRecords': 0}}
    }

    if(len(maxCountBparty) > 0):
        responseData['partyBWithMaxCount']['records'] = maxCountBparty.to_dict(
            orient='records')
        responseData['partyBWithMaxCount']['numberofRecords'] = len(
            responseData['partyBWithMaxCount']['records'])

    if(len(minCountBparty) > 0):
        responseData['partyBWithMinCount']['records'] = minCountBparty.to_dict(
            orient='records')
        responseData['partyBWithMinCount']['numberofRecords'] = len(
            responseData['partyBWithMinCount']['records'])

    if(len(usageTypeWiseMax) > 0):
        print('type of dataframe in max-usage-type:     \n',type(usageTypeWiseMax) )
        responseData['moc']['maxCount']['records'] = formatEachGrp(usageTypeWiseMax.get_group(
            'MOC'), 'max').to_dict(orient='records') if "MOC" in usageTypeWiseMax.groups else []
        responseData['moc']['maxCount']['numberofRecords'] = len(
            responseData['moc']['maxCount']['records'])
        responseData['mtc']['maxCount']['records'] = formatEachGrp(usageTypeWiseMax.get_group(
            'MTC'), 'max').to_dict(orient='records') if "MTC" in usageTypeWiseMax.groups else []
        responseData['mtc']['maxCount']['numberofRecords'] = len(
            responseData['mtc']['maxCount']['records'])
        responseData['smsmo']['maxCount']['records'] = formatEachGrp(usageTypeWiseMax.get_group(
            'SMSMO'), 'max').to_dict(orient='records') if "SMSMO" in usageTypeWiseMax.groups else []
        responseData['smsmo']['maxCount']['numberofRecords'] = len(
            responseData['smsmo']['maxCount']['records'])
        responseData['smsmt']['maxCount']['records'] = formatEachGrp(usageTypeWiseMax.get_group(
            'SMSMT'), 'max').to_dict(orient='records') if "SMSMT" in usageTypeWiseMax.groups else []
        responseData['smsmt']['maxCount']['numberofRecords'] = len(
            responseData['smsmt']['maxCount']['records'])

    if(len(usageTypeWiseMin) > 0):
        responseData['moc']['minCount']['records'] = formatEachGrp(usageTypeWiseMin.get_group(
            'MOC'), 'min').to_dict(orient='records') if "MOC" in usageTypeWiseMin.groups else []
        responseData['moc']['minCount']['numberofRecords'] = len(
            responseData['moc']['minCount']['records'])
        responseData['mtc']['minCount']['records'] = formatEachGrp(usageTypeWiseMin.get_group(
            'MTC'), 'min').to_dict(orient='records') if "MTC" in usageTypeWiseMin.groups else []
        responseData['mtc']['minCount']['numberofRecords'] = len(
            responseData['mtc']['minCount']['records'])
        responseData['smsmo']['minCount']['records'] = formatEachGrp(usageTypeWiseMin.get_group(
            'SMSMO'), 'min').to_dict(orient='records') if "SMSMO" in usageTypeWiseMin.groups else []
        responseData['smsmo']['minCount']['numberofRecords'] = len(
            responseData['smsmo']['minCount']['records'])
        responseData['smsmt']['minCount']['records'] = formatEachGrp(usageTypeWiseMin.get_group(
            'SMSMT'), 'min').to_dict(orient='records') if "SMSMT" in usageTypeWiseMin.groups else []
        responseData['smsmt']['minCount']['numberofRecords'] = len(
            responseData['smsmt']['minCount']['records'])


    return responseData


def formatEachGrp(df, max_or_min):
    app.logger.info(f'group df: \n{df}')
    df.drop(columns=['usageType'], inplace=True)
    if max_or_min=='max' :
        df = df.nlargest(numberOfmsisdns, 'usageTypeCount')
        app.logger.info(f'group df after {max_or_min} sort: \n{df}')

        return df
    if max_or_min=='min':
        df = df.nsmallest(numberOfmsisdns, 'usageTypeCount')
        app.logger.info(f'group df after {max_or_min} sort: \n{df}')
        return df

    
    return df


def formatDataByUsagetype(df, max_or_min):

    if (not df.empty):
        df = df[['_source.party_a', '_source.party_b',
                 '_source.usage_type', '_source.call_duration']]
        df.columns = ['partyA', 'partyB', 'usageType', 'callDuration']

        aggrUsageType = df.groupby(['usageType', 'partyB']).agg({
            'usageType': 'size',
            'callDuration': 'sum'
        })

        app.logger.info(f'df after aggregation: \n{aggrUsageType}')

        aggrUsageType.rename(
            columns={"usageType": "usageTypeCount"}, inplace=True)
        aggrDf = aggrUsageType.reset_index()

        app.logger.info(f'df after aggregation reset: \n{aggrDf}')

        grpByUsagetypeDf = aggrDf.groupby('usageType')

        return grpByUsagetypeDf

    return pd.DataFrame([])


def formatDataforMaxMinCount(df, max_or_min):

    if (not df.empty):
        df = df[['_source.party_a', '_source.party_b',
                 '_source.usage_type', '_source.call_duration']]
        df.columns = ['partyA', 'partyB', 'usageType', 'callDuration']
        # df = df[(df['usageType'] == 'MOC') | (df['usageType'] == 'MTC')]
        # app.logger.info(f'df for MOC and MOT: \n {df}')

        aggrByPartyB = df.groupby(['partyB']).agg({
            'usageType': 'size',
            'callDuration': 'sum'
        })

        aggrByPartyB.rename(
            columns={"usageType": "usageTypeCount"}, inplace=True)

        aggrByPartyB.reset_index(inplace=True)

        app.logger.info(f'df after aggregation: \n{aggrByPartyB}')

        if(max_or_min is "max"):
            return aggrByPartyB.nlargest(numberOfmsisdns, 'usageTypeCount')
            
        if(max_or_min is "min"):
            return aggrByPartyB.nsmallest(numberOfmsisdns, 'usageTypeCount')
            

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
