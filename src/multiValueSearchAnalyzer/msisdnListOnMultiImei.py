from src.analyzedDataProvider import msisdnListOnImei
from flask import current_app as app
from src.util import msisdnPrefix
import json

def getResponse(body):
   
    df = msisdnListOnImei.getData(body=body)
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
        for imei in df.groups:
            singleResponse = {}
            singleResponse["key"] = imei
            singleResponse["msisdnWithTime"]=  json.loads(formateEachGrp(df.get_group(imei)).to_json(orient='records')) 
            singleResponse["numberOfRecords"] = len(singleResponse["msisdnWithTime"])
            responseData["data"]["records"].append(singleResponse)

    responseData["data"]["numberOfRecords"] = len(responseData["data"]["records"])

    return responseData

def formateEachGrp(df):
    formatedGrpDf = msisdnListOnImei.formatData(df)
    app.logger.info(f'grp df after process: {formatedGrpDf}')
    return formatedGrpDf

def formatData(df):
    if not df.empty:
        grpbyDf = df.groupby(['_source.imei_number'])
        return grpbyDf

    return df

