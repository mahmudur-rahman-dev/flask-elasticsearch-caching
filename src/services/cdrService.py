from src.responseBuilder import cdrResponseBuilder
from src.responseBuilder import errorResponseBuilder;
from src.reportGenerator import searchSummaryGenerator

from src.constant import constant
from src.services import redisPublishService
from src.dbService import esService as es
from src.util import dateTime
from src.util import msisdnPrefix
from flask import current_app as app
def getCDR(body):
    status = True
    response = None
    searchTime = dateTime.getCurrentTimestampMS()
    try:
        if body['searchCriteria'] == 1:
            body['searchValue'] = msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(
                body['searchValue'])
        esSearchCriteriaDict = {"MSISDN": "party_a",
                                "IMEI": "imei_number", "IMSI": "imsi"}
        esSearchCriteria = esSearchCriteriaDict[constant.getSearchCriteriaDict()[
            body["searchCriteria"]]]
        
        startDate = dateTime.convertToYearMonthDay(body["startDate"])
        endDate = dateTime.convertToYearMonthDay(body["endDate"])

        esBody = {"query": {"bool": {"must": [{"match": {esSearchCriteria: body["searchValue"]}}, {"range": {"event_time": {
            "gte": startDate, "lt": endDate}}}], "must_not": [], "should": []}}}

        esData = es.search(index="cdr", body=esBody)
        app.logger.info(f"Data Received from Elastic Search for CDR : {len(esData)}")
        response = cdrResponseBuilder.getCdrResponse(body, esData)
    except Exception as e:
        app.logger.exception(e)
        response = errorResponseBuilder.getErrorResponse(body, e)
        status = False
    response = redisPublishService.publishToRedis(
        body, response)
    searchSummaryGenerator.saveSearchSummary(
        body, response, searchTime, status, response["type"])
    return response
