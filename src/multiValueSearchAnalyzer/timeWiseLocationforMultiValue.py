from src.analyzedDataProvider import locationWithTime
from flask import current_app as app
from src.util import msisdnPrefix
import json

getGrpByColumn = {
    'MSISDN' : '_source.party_a',
    'IMEI' : '_source.imei_number'
}

def getResponse(body):
    body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
        i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']
    df = locationWithTime.getData(body=body)
    app.logger.info(f'data from es: \n {df}')
    formatedDf = formatData(df, body)
    app.logger.info(f'formated df: \n {formatedDf}')
    return makeResponse(formatedDf, body)


def makeResponse(df, body):
    responseData = {
        "data": {"records": [], "numberOfRecords": 0},
        "error": None
    }
    if len(df) > 0:
        for value in df.groups:
            singleResponse = {}
            singleResponse["key"] = value
            singleResponse["locationsWithTime"] = json.loads(
                formateEachGrp(df.get_group(value), body).to_json(orient='records'))
            singleResponse["numberOfRecords"] = len(
                singleResponse["locationsWithTime"])
            responseData["data"]["records"].append(singleResponse)

    responseData["data"]["numberOfRecords"] = len(
        responseData["data"]["records"])

    return responseData


def formateEachGrp(df, body):
    return locationWithTime.formatData(df, body)


def formatData(df, body):
    if not df.empty:
        grpbyDf = df.groupby([getGrpByColumn[body['searchCriteria']]])
        return grpbyDf

    return df
