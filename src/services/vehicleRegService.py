from src.util import dateTime
from src.reportGenerator import searchSummaryGenerator
from src.responseBuilder import vehicleRegistrationResponseBuilder, errorResponseBuilder
from . import backendService
from . import redisPublishService
from src.dbService import esService as es
from src.constant import constant
from flask import current_app as app
from . import caseManagmentService
def getVehicleRegistration(body):
    status = True
    response = None
    body['requestType'] ="VEHICLEREGISTRATION"
    
    
    if not app.config["FROM_CACHE"]:
        backendService.postToMno(body, "vehicle-registration")
        return ''
    try:
        searchTime = dateTime.getCurrentTimestampMS()
        body["selectionCriteria"] = constant.SelectionCriterias['VEHICLE_REGISTRATION']
        esSearchCriteria = 'vehicle_registration_number.keyword'
        esSearchValue = body['zone']+'-' + \
            body['series']+'-'+body['vehicleNumber']
        
        esQueryBody = {"query": {"bool": {"must": [{"match": {esSearchCriteria: esSearchValue}}], "must_not": [
        ], "should": []}}}
        esData = es.search("vehicle", esQueryBody)
        app.logger.info(f"Data Received from Elastic Search for Vehicle Registration: {esData}")
        if len(esData) == 0:
            backendService.postToMno(body, "vehicle-registration")
            return ''
        response = vehicleRegistrationResponseBuilder.getVehicleRegistrationResponse(
            esData)
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
