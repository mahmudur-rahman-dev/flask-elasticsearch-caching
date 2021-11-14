import pandas as pd
import numpy as np
import json
from src.dbService import esService
from src.constant import constant
from datetime import datetime
from flask import current_app as app
from src.util import msisdnPrefix




def getResponse(body):
    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]

    # body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
    #     i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']
    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] == 'MSISDN' else body['searchValue']

    df = getData(body)
    app.logger.info(f'data from es for request: {body} \n{df}')
    formatedDf = formatData(df, body)
    app.logger.info(f'formated df for request: {body} \n{formatedDf}')
    return makeResponse(formatedDf)


def makeResponse(df):

    locationsWithTime = df.to_dict(orient="records")
    dataSize = len(locationsWithTime)
    locationsWithTime = {
        "locationsWithTime": locationsWithTime,
        "numberofRecords": dataSize
    }

    return locationsWithTime


def getData(body):

    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)

    return df


def formatData(df, body):
    if (not df.empty):
        df = df[['_source.party_a', '_source.imei_number', '_source.lac_start_a', '_source.ci_start_a', '_source.bts_id', '_source.bts.latitude',
                 '_source.bts.longitude', '_source.bts.address', '_source.event_time', '_source.call_duration']]

        df = df.replace("", np.nan).dropna(subset=['_source.lac_start_a', '_source.ci_start_a', '_source.bts_id',
                                                   '_source.bts.latitude', '_source.bts.longitude', '_source.event_time'])

        """
        Giving consecutive same lac same subgroup depending of search-value
        """
        df['lacSubgroup'] = (df[[constant.cdrEsSourceColumn[body['searchCriteria']], '_source.lac_start_a']] != df[[
                             constant.cdrEsSourceColumn[body['searchCriteria']], '_source.lac_start_a']].shift(1)).any(axis=1).cumsum()

        df.rename(columns={
            '_source.party_a': 'msisdn',
            '_source.imei_number': 'imei',
            '_source.lac_start_a': 'lac',
            '_source.ci_start_a': 'cellId',
            '_source.bts_id': 'btsId',
            '_source.bts.latitude': 'btsLatitude',
            '_source.bts.longitude': 'btsLongitude',
            '_source.bts.address': 'btsAddress',
            '_source.event_time': 'eventTime',
            '_source.call_duration': 'totalCallDurationS'
        }, inplace=True)

        df['dateTime'] = pd.to_datetime(df['eventTime'], format='%Y%m%d%H%M%S')

        dfgrpBylac = df.groupby(['lacSubgroup', 'cellId']).agg({
            'msisdn': 'first',
            'imei': 'first',
            'lac': 'first',
            'eventTime': 'count',
            'btsLatitude': 'first',
            'btsLongitude': 'first',
            'btsAddress': 'first'
        })
        lacWithLocation = dfgrpBylac.sort_values(['lacSubgroup', 'eventTime'], ascending=(
            True, False)).reset_index().drop_duplicates('lacSubgroup')

        grpBylacSubgrp = df.groupby('lacSubgroup')

        lacWithTime = pd.DataFrame({'lac': grpBylacSubgrp['lac'].first(),
                                    'lastCdrTime': grpBylacSubgrp.dateTime.first(),
                                    'firstCdrTime': grpBylacSubgrp.dateTime.last(),
                                    'totalCdrs': grpBylacSubgrp.size(),
                                    'totalCallDurationS': grpBylacSubgrp['totalCallDurationS'].sum()})

        lacWithTime.loc[lacWithTime['lastCdrTime'] == lacWithTime['firstCdrTime'],
                        'lastCdrTime'] = lacWithTime['firstCdrTime'] + pd.to_timedelta(lacWithTime['totalCallDurationS'], unit='s')

        timeWiseLocdf = pd.merge(
            lacWithLocation, lacWithTime, on="lacSubgroup")
        timeWiseLocdf.rename(columns={'lac_x': 'lac'}, inplace=True)
        timeWiseLocdf.drop(
            columns=['lac_y', 'eventTime', 'lacSubgroup'], inplace=True)

        return timeWiseLocdf

    return pd.DataFrame([])


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime(
        "%Y%m%d%H%M%S") if 'startDate' in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime(
        "%Y%m%d%H%M%S") if 'endDate' in body else None
    selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper(
    )]
    app.logger.info(
        f' selection criteria of for request {body} is {selectionCriteria}')

    esQuery = {
        "sort": [
            {
                selectionCriteria+".keyword": "desc"
            },

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
            "imei_number",
            "event_time",
            "lac_start_a",
            "ci_start_a",
            "bts_id",
            "bts.latitude",
            "bts.longitude",
            "bts.address",
            "call_duration"
        ]

    }
    return esQuery
