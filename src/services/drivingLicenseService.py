from src.util import dateTime
from src.reportGenerator import searchSummaryGenerator
from src.responseBuilder import drivingLicenseResponseBuilder, errorResponseBuilder
from src.constant import constant
from . import backendService
from . import redisPublishService
from src.dbService import esService as es
from flask import current_app as app
from . import caseManagmentService

def getDrivingLicense(body):
    status = True
    response = None
    body['requestType'] = "DrivingLicense"
    
    
    if not app.config["FROM_CACHE"]:
        backendService.postToMno(body, "driving-license")
        return ''
    try:
        searchTime = dateTime.getCurrentTimestampMS()
        esSearchCriteria = constant.getDrivingLicenseSearchCriteria()[
            body['parameterType']]
        body["selectionCriteria"] = constant.SelectionCriterias[ body['parameterType']]
        esQueryBody = {"query": {"bool": {"must": [{"match": {esSearchCriteria: body["parameterValue"]}}], "must_not": [
        ], "should": []}}}
        esData = es.search(index="driving-license", body=esQueryBody)

        if len(esData) == 0:
            backendService.postToMno(body, "driving-license")
            return ''

        response = drivingLicenseResponseBuilder.getDrivingLicenseResponse(
            esData)
        app.logger.info(f"Data Received from Elastic Search for Driving License:{response['data']['numberofRecordsFound']}")
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
