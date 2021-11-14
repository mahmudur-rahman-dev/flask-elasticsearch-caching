from src.util import dateTime
from src.reportGenerator import searchSummaryGenerator
from src.responseBuilder import passportResponseBuilder,errorResponseBuilder
from src.constant import constant
from . import backendService
from . import redisPublishService
from src.dbService import esService as es
from src.constant import constant
from flask import current_app as app
from . import caseManagmentService
def getPassport(body):
    status = True
    response = None
    body['requestType'] ="Passport"
    
    
    if not app.config["FROM_CACHE"]:
        backendService.postToMno(body,"passport")
        return ''
    try:
        searchTime = dateTime.getCurrentTimestampMS()

        esSearchCriteria = constant.getPassportSearchCriteria()[
            body['parameterType']]
        body["selectionCriteria"] = constant.SelectionCriterias[ body['parameterType']]
        esQueryBody = {"query": {"bool": {"must": [{"match": {esSearchCriteria: body["parameterValue"]}}], "must_not": [
        ], "should": []}}}
        esData = es.search("passport",esQueryBody)
        response = passportResponseBuilder.getPassportResponse(esData)
        app.logger.info(f"Data Received from Elastic Search for Passport:{response['data']['numberofRecordsFound']}")
        if len(esData) == 0:
            backendService.postToMno(body,"passport")
            return ''
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
    
