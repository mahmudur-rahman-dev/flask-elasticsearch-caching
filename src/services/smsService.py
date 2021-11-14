from src.constant import constant
from src.responseBuilder import smsResponseBuilder,errorResponseBuilder
from . import redisPublishService
from src.dbService import esService as es
from src.util import dateTime
from src.util import msisdnPrefix
from flask import current_app as app

def getSMS(body):
    status = True
    response = None
    try:
        if body['searchCriteria'] == 1:
            body['searchValue']= msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(body['searchValue'])
        searchTime = dateTime.getCurrentTimestampMS()
        startDate = dateTime.convertToYearMonthDay(body["startDate"])
        endDate = dateTime.convertToYearMonthDay(body["endDate"])
        esQueryBody = {"query": {"bool": {"must": [{"bool": {"minimum_should_match": 1, "should": [{"match": {"party_a": body["searchValue"]}}, {"match": {
            "party_b": body["searchValue"]}}]}}, {"range": {"event_time": {"gte": startDate, "lte": endDate}}}]}}}
        esData = es.search("sms",esQueryBody)
        app.logger.info(f"Data Received from Elastic Search for SMS:{esData}")
        response =  smsResponseBuilder.getSMSResponse(body, esData)
    except Exception as e:
        app.logger.exception(e)
        response = errorResponseBuilder.getErrorResponse(body, e)
        status = False
    response = redisPublishService.publishToRedis(
        body, response)
    searchSummaryGenerator.saveSearchSummary(
        body, response, searchTime, status, response["type"])
    return response
