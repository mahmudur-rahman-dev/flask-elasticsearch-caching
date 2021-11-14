import pandas as pd
import json
from src.constant import constant
from datetime import datetime
from src.dbService import esService
from src.constant.timePeriods import TimePeriods
from flask import current_app as app
from src.util import msisdnPrefix


columnBySearchCriteria = {
    'MSISDN': 'partyA',
    'IMEI': 'imei'
}


def getResponse(body):

    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]

    # body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
    #     i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']

    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f'data from es for request: {body} \n {df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated dataframe for request: {body}: \n {formatedDf}')
    return makeResponse(formatedDf, body)


def makeResponse(df, body):

    locationTimePeriod = dict()

    for value in constant.timePeriods.values():

        locationTimePeriod[constant.timePeriodsIncc[value]] = {
            "timePeriod": getTimePeriodefinition(value),
            "records": [],
            "numberofRecords": 0
        }
        if(len(df) > 0):
            locationTimePeriod[constant.timePeriodsIncc[value]]['records'] = json.loads(
                getLocInTimePeriod(df.get_group(value), body).to_json(orient="records")) if value in df.groups else []
            locationTimePeriod[constant.timePeriodsIncc[value]]["numberofRecords"] = len(
                locationTimePeriod[constant.timePeriodsIncc[value]]["records"])

    return locationTimePeriod


def getTimePeriodefinition(timePeriodName):
    enumValue = TimePeriods[timePeriodName]
    return enumValue.value


def getLocInTimePeriod(df, body):

    if(not df.empty):

        df['lacSubgroup'] = (df['lac'] != df['lac'].shift(1)).cumsum()

        app.logger.info(f'df after adding lac-sub-grp: \n{df}')
        dfgrpBylac = df.groupby(['lacSubgroup', 'cellId']).agg({
            'partyA': 'first',
            'imei': 'first',
            'lac': 'first',
            'eventTime': 'count',
            'btsLatitude': 'first',
            'btsLongitude': 'first',
            'btsAddress': 'first'
        })
        app.logger.info(f'df after group by lacsub and cell: \n {dfgrpBylac}')

        lacWithLocation = dfgrpBylac.sort_values(['lacSubgroup', 'eventTime'], ascending=(
            True, False)).reset_index().drop_duplicates('lacSubgroup')

        app.logger.info(
            f'df after group by lacsub and cell having most cdrs: \n {lacWithLocation}')

        grpbyLacSubgrp = df.groupby('lacSubgroup')
        lacWithTime = pd.DataFrame({'lac': grpbyLacSubgrp['lac'].first(),
                                    'lastCdrTime': grpbyLacSubgrp.dateTime.first(),
                                    'firstCdrTime': grpbyLacSubgrp.dateTime.last(),
                                    'totalCdrs': grpbyLacSubgrp.size()})
        app.logger.info(
            f'df after group by lacsub and first cdr time and last cdr time: \n {lacWithTime}')

        timeWiseLocdf = pd.merge(
            lacWithLocation, lacWithTime, on="lacSubgroup")
        timeWiseLocdf.rename(columns={'lac_x': 'lac'}, inplace=True)
        timeWiseLocdf.drop(
            columns=['lac_y', 'eventTime', 'lacSubgroup'], inplace=True)
        app.logger.info(
            f'df for location with time interval: \n {timeWiseLocdf}')
        return timeWiseLocdf
    return df


def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)
    return df


def formatData(df):

    if (not df.empty):
        df = df[['_source.party_a', '_source.imei_number', '_source.party_b', '_source.event_time', '_source.lac_start_a', '_source.ci_start_a',
                 '_source.bts.latitude', '_source.bts.longitude', '_source.bts.address']]
        df.columns = ['partyA', 'imei', 'partyB', 'eventTime', 'lac', 'cellId',
                      'btsLatitude', 'btsLongitude', 'btsAddress']
        df = df.dropna(
            subset=['lac', 'cellId', 'btsLatitude', 'btsLongitude', 'eventTime'])

        df['dateTime'] = pd.to_datetime(
            df['eventTime'], format='%Y%m%d%H%M%S')
        df['period'] = (df['dateTime'].dt.hour % 24 + 4) // 4
        df['period'].replace(constant.timePeriods, inplace=True)
        grpByPeriod = df.groupby(['period'])
        return grpByPeriod

    return pd.DataFrame([])


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime(
        "%Y%m%d%H%M%S") if 'startDate' in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime(
        "%Y%m%d%H%M%S") if 'endDate' in body else None

    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper(
    )]

    esQuery = {
        "sort": [
            # {
            #     selectionCriteria+".keyword": "desc"
            # },
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
            "event_time",
            "lac_start_a",
            "ci_start_a",
            "bts.latitude",
            "bts.longitude",
            "bts.address",
            "party_b",
            "party_a",
            "imei_number"

        ]
    }

    return esQuery
