from flask import current_app as app
import asyncio
import threading
from . import spendingTimeLoc
from . import msisdnListOnImei
from . import imeiListOnMsisdn
from . import locationWithTime
from . import cdrUsageTypeFre
from . import partyBwithMaxMinDurTotal
from . import partyBwithMaxMinDur
from . import partyBwithMaxMinCdrCount
from . import timePeriodWiseLoc
from . import datePeriodHeatMapProvider
from . import timePeriodWiseUsageType
from . import companySMS
from . import cdrMapPathDataProvider
from . import deviceInfoProvider

from src.dbService import cdrSearch
import pandas as pd

def getResponse(body):
    # result  = asyncio.get_event_loop().run_until_complete(getDataAsynchronously(body))
    result = asyncio.run(getDataAsynchronously(body)) 
    # result = await getDataAsynchronously(body)
    # app.logger.info(f'{result}')
    # loop.close()
    return {"data": result, "error": None}

async def getDataAsynchronously(body):
    tasks = []
    for element in body:
        task = asyncio.create_task(getAllResponse(element))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    # app.logger.info(f'{results}')
    # data = []
    # for result in results:
    #     data.append(result.response)
    return results

async def getAllResponse(body):
    # name = threading.currentThread().getName()
    # app.logger.info(f'------------------------------------thread nama {name}--------------------------------------\n')

    # esData = await cdrSearch.getCdrFromEsInTimeRange(body['searchCriteria'], body['searchValue'], body['startDate'], body['endDate'])
    # df = pd.json_normalize(esData)

    response={
        'searchedWith' : body['searchValue']
    }
    response['analyzedData'] = {
        # "duartionWiseLocation": spendingTimeLoc.getResponse(body),
        # "msisdnsWithTime" : msisdnListOnImei.getResponse(body),
        # "imeiWithTime" : imeiListOnMsisdn.getResponse(body),
        # "locationsWithTime" : locationWithTime.getResponse(body),
        # "usageTypeSummary" : cdrUsageTypeFre.getResponse(body),
        # "bPartiesWithMaxAndMinTotalDuration" : partyBwithMaxMinDurTotal.getResponse(body),
        # "bPartiesWithMaxAndMinDuration" : partyBwithMaxMinDur.getResponse(body),
        # "bPartiesWithMaxAndMinCdrCount" : partyBwithMaxMinCdrCount.getResponse(body),
        # "timePeriodWiseLocation" : timePeriodWiseLoc.getResponse(body),
        # "dateAndTimePeriodWiseDataByCdrCount" : datePeriodHeatMapProvider.getResponse(body, "cdr-count"),
        # "dateAndTimePeriodWiseDataByCdrDuration" : datePeriodHeatMapProvider.getResponse(body, "total-duration"),
        # "timePeriodWiseUsageType" : timePeriodWiseUsageType.getResponse(body),
        # "companrySms" : companySMS.getResponse(body),
        # "pathOnMap" : cdrMapPathDataProvider.getResponse(body),
        # "deviceInformation" : deviceInfoProvider.getResponse(body)

        "duartionWiseLocation": await getSpendingTimeWiseLocation(body),
        "msisdnsWithTime" : await getMsisdnListOnImei(body),
        "imeiWithTime" : await getImeiListOnMsisdn(body),
        "locationsWithTime" : await getTimeWiseLocation(body),
        "usageTypeSummary" : await getUsageTypeCount(body),
        "bPartiesWithMaxAndMinTotalDuration" : await getBpartiesWithMaxMinTotalDuartion(body),
        "bPartiesWithMaxAndMinDuration" : await getBparitesWithMaxMinDuration(body),
        "bPartiesWithMaxAndMinCdrCount" : await getBparitesWithMaxMinCdrCount(body),
        "timePeriodWiseLocation" : await getTimePeriodWiseLocation(body),
        "dateAndTimePeriodWiseDataByCdrCount" : await getDateTimeHeatMapData(body, "cdr-count"),
        "dateAndTimePeriodWiseDataByCdrDuration" : await getDateTimeHeatMapData(body, "total-duration"),
        "timePeriodWiseUsageType" : await getTimePeriodWiseUsageType(body),
        "companrySms" : await getCompanySms(body),
        "pathOnMap" : await getPathOnMapData(body),
        "deviceInformation" : await getDeviceInformation(body)
    }

    return response


async def getSpendingTimeWiseLocation(body):
    return spendingTimeLoc.getResponse(body)

async def getImeiListOnMsisdn(body):
    return imeiListOnMsisdn.getResponse(body)
   
async def getMsisdnListOnImei(body):
    return msisdnListOnImei.getResponse(body)

async def getTimeWiseLocation(body):
    return locationWithTime.getResponse(body)

async def getUsageTypeCount(body):
    return cdrUsageTypeFre.getResponse(body)

async def getBpartiesWithMaxMinTotalDuartion(body):
    return partyBwithMaxMinDurTotal.getResponse(body)

async def getBparitesWithMaxMinDuration(body):
    return partyBwithMaxMinDur.getResponse(body)

async def getBparitesWithMaxMinCdrCount(body):
    return partyBwithMaxMinCdrCount.getResponse(body)

async def getTimePeriodWiseLocation(body):
    return timePeriodWiseLoc.getResponse(body)

async def getDateTimeHeatMapData(body, generateBy):
    return datePeriodHeatMapProvider.getResponse(body, "cdr-count")

async def getTimePeriodWiseUsageType(body):
    return timePeriodWiseUsageType.getResponse(body)

async def getCompanySms(body):
    return  companySMS.getResponse(body)

async def getPathOnMapData(body):
    return cdrMapPathDataProvider.getResponse(body)

async def getDeviceInformation(body):
    return deviceInfoProvider.getResponse(body)