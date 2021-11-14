from src.util import dateTime
from src.responseBuilder import birthRegResponseBuilder,errorResponseBuilder
from src.reportGenerator import searchSummaryGenerator
from . import backendService
from . import redisPublishService
from src.dbService import esService as es
from src.constant.constant import SelectionCriterias
from . import caseManagmentService
from flask import current_app as app

def getBirthRegistration(body):
    status = True
    response = None
    body['requestType'] ="BirthRegistration"

    if  not app.config["FROM_CACHE"]:
        backendService.postToMno(body,"birth-registration")
        return ''


    try:
        searchTime = dateTime.getCurrentTimestampMS()
      
        body["selectionCriteria"] = SelectionCriterias['BIRTH_REGISTRATION']
        esSearchCriteria = "birth_reg_no"
        esQueryBody = {"query": {"bool": {"must": [{"match": {esSearchCriteria: body["birthRegNo"]}}], "must_not": [
        ], "should": []}}}
        esData = es.search(index="birth_registration", body=esQueryBody)
        app.logger.info(f"Data Received from Elastic Search for Birth Registration: {esData}")
        if len(esData) == 0:
            backendService.postToMno(body,"birth-registration")
            return ''
        response = birthRegResponseBuilder.getBirthRegResponse(esData)

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
        