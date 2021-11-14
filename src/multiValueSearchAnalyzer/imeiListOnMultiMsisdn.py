from src.analyzedDataProvider import imeiListOnMsisdn
from flask import current_app as app
from src.util import msisdnPrefix
import json
def getResponse(body):
    body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(i) for i in body['searchValues']]
    df = imeiListOnMsisdn.getData(body=body)
    app.logger.info(f'data from es: \n {df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df: \n {formatedDf}')
    return makeResponse(formatedDf)

def makeResponse(df):
    responseData = {
        "data" : {"records": [], "numberOfRecords": 0},
        "error" : None
    }
    if len(df)>0:
        for msisdn in df.groups:
            singleResponse = {}
            singleResponse["key"] = msisdn
            singleResponse["imeiWithTime"]= json.loads(formateEachGrp(df.get_group(msisdn)).to_json(orient='records')) 
            singleResponse["numberOfRecords"] = len(singleResponse["imeiWithTime"])
            responseData["data"]["records"].append(singleResponse)

    responseData["data"]["numberOfRecords"] = len(responseData["data"]["records"])

    return responseData

def formateEachGrp(df):
    return imeiListOnMsisdn.formatData(df)

def formatData(df):
    if not df.empty:
        grpbyDf = df.groupby(['_source.party_a'])
        return grpbyDf

    return df

