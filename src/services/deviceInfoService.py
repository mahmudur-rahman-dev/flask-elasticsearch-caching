from src.constant import constant
from src.responseBuilder import esafResponseBuilder, errorResponseBuilder
from . import backendService
from . import redisPublishService
from src.dbService import esService as es
from src.util import backendQueryBody
from src.util import dateTime
from src.util import msisdnPrefix
from src.reportGenerator import searchSummaryGenerator
from flask import current_app as app
from . import caseManagmentService

from src.analyzedDataProvider import deviceInfoProvider
from src.responseBuilder import deviceInfoResponseBuilder

def getDeviceInformation(body):
    status = True
    response = None

    try:
        if body['searchCriteria'] == 1:
            body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
                body['searchValue'])
        searchTime = dateTime.getCurrentTimestampMS()
        
        newBody = {
            "searchCriteria" : constant.getSearchCriteriaDict()[body["searchCriteria"]],
            "searchValue" : body["searchValue"]
        }

        esData = deviceInfoProvider.getResponse(newBody)
        response = deviceInfoResponseBuilder.getDeviceInfoResponse(body, esData)
        if ('discoveryId' in body) and ('unifiedViewerId' in body) and (body['unifiedViewerId'] is not None) and (body['discoveryId'] is not None):
            caseManagmentService.insertDataToDipUnifiedViewerSearchSummary(body, response['type'])
    except Exception as e:
        app.logger.exception(e)
        response = errorResponseBuilder.getErrorResponse(body, e)
        status = False
    response = redisPublishService.publishToRedis(
        body, response)
    searchSummaryGenerator.saveSearchSummary(
        body, response, searchTime, status, response["type"])
    return response
