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

def getESAF(body):
    status = True
    response = None

    try:
        if body['searchCriteria'] == 1:
            body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
                body['searchValue'])
        searchTime = dateTime.getCurrentTimestampMS()
        newBody = backendQueryBody.getBody(body)

        app.logger.info(f'body for esaf request: {newBody} from cache variable: app.config["FROM_CACHE"]')
        
        if not app.config["FROM_CACHE"]:
            backendService.postToMno(newBody, "mno")
            return ''
        else:
            esSearchCriteriaDict = {"MSISDN": "phone", "NID": "nid"}
            esSearchCriteria = esSearchCriteriaDict[constant.getSearchCriteriaDict()[body["searchCriteria"]]]

            esQueryBody = {
                "query": {
                    "bool": {
                        "must":
                        [
                            {
                                "match": {esSearchCriteria: body["searchValue"]}
                            },
                            {
                                "match": {"case_id": body["caseId"]}
                            }
                        ],
                        "must_not": [],
                        "should": [],
                    }
                }
            }

            app.logger.info(f'query generated for esaf service: {esQueryBody}')

            body["selectionCriteria"] = body["searchCriteria"]
            esData = es.search("esaf", esQueryBody)
            app.logger.info(f"Data Received from Elastic Search for ESAF: {str(esData)}")

            if len(esData) == 0:
                backendService.postToMno(newBody, "mno") # Retrieves esaf response from backend if not found in ES.
                return ''
            response = esafResponseBuilder.getEsafResponse(body, esData)
            if ('discoveryId' in body) and ('unifiedViewerId' in body) and (body['unifiedViewerId'] is not None) and (body['discoveryId'] is not None):
                caseManagmentService.insertDataToDipUnifiedViewerSearchSummary(body, response['type'])
            return response
        
    except Exception as e:
        app.logger.exception(e)
        response = errorResponseBuilder.getErrorResponse(body, e)
        status = False
    response = redisPublishService.publishToRedis(body, response)
    searchSummaryGenerator.saveSearchSummary(body, response, searchTime, status, response["type"])
    return response