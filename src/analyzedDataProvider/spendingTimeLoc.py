import pandas as pd
import json
from src.dbConfig import dbConfig
from src.constant import constant
from sklearn.preprocessing import MinMaxScaler
import random
from flask import current_app as app


from . import locationWithTime
from src.util import msisdnPrefix

columnBySearchCriteria = {
    'MSISDN' : 'msisdn',
    'IMEI' : 'imei'
}

def getResponse(body):
    
    # if 'searchValue' in body:
    #     body['searchValues'] = [body['searchValue']]

    # body['searchValues'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
    #     i) for i in body['searchValues']] if body['searchCriteria'] == 'MSISDN' else body['searchValues']

    body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue']) if body['searchCriteria'] is 'MSISDN' else body['searchValue']
    df = getData(body)
    app.logger.info(f"data from es for most spending time for request: {body} \n{df}") 
    formatedDf =  formatData(df, body)
    heatMapDf = prepareDataForheatMap(formatedDf)
    app.logger.info(f"heat map data for request: {body} \n {heatMapDf}")
    return makeResponse(heatMapDf)


def makeResponse(df):
    locationsWithDurationss = json.loads(df.to_json(orient = "records"))
    dataSize = len(locationsWithDurationss)

    locationsWithDuration = {
        "locationsWithDuration": locationsWithDurationss,
        "numberofRecords" : dataSize
    }

    return locationsWithDuration


def getData(body):
    data = locationWithTime.getResponse(body)['locationsWithTime']
    df = pd.DataFrame(data)
    return df


def formatData(df, body):
    if (not df.empty):
        app.logger.info(f'{df}')
        df['spentTimems'] = df['lastCdrTime'] - df['firstCdrTime']
        totalspentTime = df.groupby([columnBySearchCriteria[body['searchCriteria']],'lac', 'cellId']).agg({
            'spentTimems': 'sum',
            'btsLatitude': 'first',
            'btsLongitude': 'first',
            'btsAddress': 'first',
            'totalCdrs': 'sum'
        }).sort_values(['spentTimems'], ascending=(False)).reset_index()
        app.logger.info(f'{totalspentTime}')
        return totalspentTime
    
    return pd.DataFrame([])





def prepareDataForheatMap(df):

    if(not df.empty):
        
        df['spentTimeLong'] = df['spentTimems'].astype('int64')
        scaler=MinMaxScaler(feature_range=(1,50))
        df['normalizedDuration'] = scaler.fit_transform(df['spentTimeLong'].values.reshape(-1, 1))
        df['normalizedDuration'] = df['normalizedDuration'].astype('int64')
        
        distantVal = 0.0005
        heatMapdf = pd.DataFrame()

        for i in range(len(df)):
            heatMapdf = heatMapdf.append(df.iloc[i],ignore_index=True)
            
            for j in range(0,df.iloc[i]["normalizedDuration"]):
                row = df.iloc[i]
                heatMapdf = heatMapdf.append(row,ignore_index=True)
                heatMapdf.tail(1)['btsLatitude'] =  heatMapdf.tail(1)['btsLatitude'] + random.uniform(-distantVal, distantVal)
                heatMapdf.tail(1)['btsLongitude'] =  heatMapdf.tail(1)['btsLongitude'] + random.uniform(-distantVal, distantVal)

        return heatMapdf
    return df

