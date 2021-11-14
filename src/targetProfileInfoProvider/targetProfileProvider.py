
from src.services import esafService
from src.dbService import esService
from . import targetEsafInfoProvider
from src.analyzedDataProvider import deviceInfoProvider
from src.analyzedDataProvider import cdrMapPathDataProvider
from src.analyzedDataProvider import cdrUsageTypeFre
from flask import current_app as app

import pandas as pd

def getResponse(body):
    return makeResponse(body)

def makeResponse(body):
    response = {
        'esafInfo' : getEsafInfo(body),
        'deviceInfo' : getDeviceInfo(body),
        'timeDuration' : {'startDate' : body['startDate'] if 'startDate' in body else None,
                            'endDate': body['endDate'] if 'endDate' in body else None },
        'totalCount' : getTotalUsageTypeWiseCount(body),
        'lastCallLocation' : getLastCallLocation(body)

    }

    return response

def getEsafInfo(body):
    esafResponse = targetEsafInfoProvider.getResponse(body)
    return 

def getDeviceInfo(body):
    # body = {
    #     'searchCriteria' : 'MSISDN',
    #     'searchValue' : body['msisdn']
    # }
    return deviceInfoProvider.getResponse(body)

def getLastCallLocation(body):
    # body['searchCriteria'] = 'MSISDN'
    # body['searchValue'] = body['msisdn']
    response = cdrMapPathDataProvider.getResponse(body)['records']
    if len(response)>0:
        return response[0]
    return None

def getTotalUsageTypeWiseCount(body):
    # body['searchCriteria'] = 'MSISDN'
    # body['searchValue'] = body['msisdn']
    response = cdrUsageTypeFre.getResponse(body=body)['usageTypeSummary']
    print(type(response))
    if response:
        dataframe = pd.DataFrame(response)
        app.logger.info(f'dataframe for total count: \n{dataframe}')
        return {
            'moc' : sum(dataframe['MOC']),
            'mtc' : sum(dataframe['MTC']),
            'smsmo' : sum(dataframe['SMSMO']),
            'smsmt' : sum(dataframe['SMSMT'])
        }
    else:
        return None



