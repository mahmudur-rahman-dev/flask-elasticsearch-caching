from datetime import datetime
from src.util import dateTime
from src.dbService import esService as es
from src.responseBuilder import nidResponseBuilder,errorResponseBuilder
from src.reportGenerator import searchSummaryGenerator
from . import backendService
from . import redisPublishService
from src.constant import constant
from flask import current_app as app
from . import caseManagmentService
# import time

def getEsSearchCriteria(body):
    return "nid_"+str(len(body["nidNumber"]))+"_digit"


def getNid(body):

    status = True
    response = None
    body['requestType'] ="Nid"
    
    app.logger.info('request for nid scenario-mode with body {body}')

    if not app.config["FROM_CACHE"]:
        backendService.postToMno(body, "nid")
        app.logger.info('request for nid scenario-mode with body {body}. \n called backend for data')
        return ''

    try:

        searchTime = dateTime.getCurrentTimestampMS()
        body["selectionCriteria"] = constant.SelectionCriterias['NID']
        esSearchCriteria = getEsSearchCriteria(body)
        esQueryBody = {"query": {"bool": {"must": [{"match": {esSearchCriteria: body["nidNumber"]}}], "must_not": [
        ], "should": []}}}
        esData = es.search("nid", esQueryBody)

        app.logger.info('query generated for nid search for es: {esData}')

        if len(esData) == 0:
            backendService.postToMno(body, "nid")
            return ''

        response = nidResponseBuilder.getNidResponse(esData)
        app.logger.info(f"Data Received from Elastic Search for NID: {len(esData)}")
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
