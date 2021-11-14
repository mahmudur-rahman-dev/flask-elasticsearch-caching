import requests
from . import backendService
from src.constant import constant
import json
from src.dbConfig import dbConfig
from src.dbService import esService as es
from src.responseBuilder import cdrResponseBuilder
from . import cdrService
from . import smsService
from flask import current_app, jsonify
import asyncio
from src.util import backendQueryBody
from src.services import redisPublishService


def findDateRageNotInStorage(dateRanges):
    startDateArr = []
    endDateArr = []
    for dateRange in dateRanges:
        if not (dateRange["fromStorage"]):
            startDateArr.append(dateRange["startDate"])
            endDateArr.append(dateRange["endDate"])
    return list(zip(startDateArr, endDateArr))


def callBackend(app, body, dateRangeNotInStorage):
    newBody = backendQueryBody.getBody(body)
    if len(dateRangeNotInStorage) == 1:
        (startDate, endDate) = dateRangeNotInStorage[0]
        newBody["startDate"] = startDate
        newBody["endDate"] = endDate
    backendService.postToMno(newBody, "mno")
    return ''


def dateRangeDecider(app, body, dateRanges):
    dateRangeNotInStorage = findDateRageNotInStorage(dateRanges)
    count = len(dateRangeNotInStorage)
    if count == 0:
        return serviceDecider(app, body)
    elif count == 1:
        try:
            callBackend(app, body, dateRangeNotInStorage)
        except:
            app.logger.info("Connecting to backend Failed")
        return serviceDecider(app, body)
    else:
        try:
            callBackend(app, body, dateRangeNotInStorage)
        except:
            app.logger.info("Connecting to backend Failed")
        return ''


def getDataRages(app, body):
    url = app.config['CASE_MANAGEMENT_URL']+str(constant.requestTypeId[body['requestType'].upper(
    )])+'/'+str(body['searchCriteria'])+'/'+body['searchValue']
    return requests.get(url=url, params={'startDate': body['startDate'], 'endDate': body['endDate']}).json()


def serviceDecider(app, body):
    requestData = body["requestType"].lower()
    es = app.es_client
    if requestData == "cdr":
        return cdrService.getCDR(body)
    elif requestData == "sms":
        return smsService.getSMS(body)


def dateRangeServices(body):
    app = current_app
    app.logger.info(f'Arrived at dateRangeServices CDR/SMS POST call')
    # Any record in search-summary-log with:
    # 1) Came from upload-service
    # and, for that record there is an entry in search-summary-log with:
    # 1) fromCache = 2
    # 2) SUCCESS flag
    # then CDR data should be retrieved from ES.
    # esQueryBody = {"query":{"bool":{"must":[{"match":{"searched_value.msisdn":body["searchValue"]}},{"match":{"searched_value.startDate":body["startDate"]}},{"match":{"searched_value.endDate":body["endDate"]}},{"match":{"data_retrieval_status":"SUCCESS"}}],"must":[{"term":{"from_cache":"2"}}],"should":[]}}}
    # esData = es.search(index="search-summary-log", body=esQueryBody)

    # app.logger.info(f'es data for cdr: \n{esData}')
    # if len(esData) > 0 and body and int(body["searchCriteria"]) == 10:
    #     print("serving from cache...")
    #     esQueryForFetchingCdr = {"query":{"bool":{"must":[{"match":{"party_a":body["searchValue"]}},{"range":{"time_stamp":{"gte":body["startDate"],"lte":body["endDate"]}}}],"must_not":[],"should":[]}}}
    #     esCdrData = es.search(index="cdr", body=esQueryForFetchingCdr)
    #     app.logger.info(f'es data lenght for cdr if data from csv : {len(esCdrData)}')
    #     response = cdrResponseBuilder.getCdrResponse(body, esCdrData)
    #     redisResponse = redisPublishService.publishToRedis(body, response)
    #     return response

    # # Now, we do not have any SUCCESS flagged data. Bye-bye CDR ES!
    # # If there is ANY record in search-summary-log that has fromCache value as 2, and a FAILURE flag, empty CDR data response should be returned.
    # esQueryBody = {"query":{"bool":{"must":[{"match":{"searched_value.msisdn":body["searchValue"]}},{"match":{"searched_value.startDate":body["startDate"]}},{"match":{"searched_value.endDate":body["endDate"]}},{"term":{"from_cache":"2"}},{"match":{"data_retrieval_status":"FAILURE"}}],"must_not":[],"should":[]}}}
    # esData = es.search(index="search-summary-log", body=esQueryBody)
    # if len(esData) > 0 and int(body["searchCriteria"]) == 10:
    #     print("No data found! Empty response is being sent as response...")
    #     app.logger.info(f'cdr data from csv saving failed')
    #     errorResponse = cdrResponseBuilder.getNoDataFoundCdrResponse(body)
    #     response = redisPublishService.publishToRedis(body, errorResponse)
    #     return errorResponse

    esQueryBody = {
        "query": {
            "bool": {
                "must":
                [
                    {
                        "match":{"searched_value.searchedWith": body["searchValue"]}
                    },
                    {
                        "match": {"start_date": body["startDate"]}
                    },
                    {
                        "match": {"end_date": body["endDate"]}
                    },
                    {
                        "term": {"from_cache": 2}
                    }
                ]
            }
        }
    }
    esData = es.search(index="search-summary-log", body=esQueryBody)
    app.logger.info(f'es data for search-summary-log: \n{esData}')

    # if len(esData) > 0 and body and int(body["searchCriteria"]) == 10:
    #     body["searchCriteria"] = int(body["searchCriteria"])
    #     return cdrService.getCDR(body)

    esQueryForCdrSmsCache = {
        "query": {
            "bool": {
                "must":
                [
                    {
                        "match":{"searched_value.searchedWith": body["searchValue"]}
                    },
                    {
                        "match": {"start_date": body["startDate"]}
                    },
                    {
                        "match": {"end_date": body["endDate"]}
                    },
                    {
                        "match": {"case_id": body["caseId"]}
                    }
                ]
            }
        }
    }

    loaded_cdr_sms_exist_in_es = es.search(index="search-summary-log", body=esQueryForCdrSmsCache)
    
    fetch_loaded_cdr_sms_from_cache = len(loaded_cdr_sms_exist_in_es) > 0

    app.logger.info(f'Loaded CDR/SMS exist in ES: {fetch_loaded_cdr_sms_from_cache}')

    if int(body["searchCriteria"]) == 10 or fetch_loaded_cdr_sms_from_cache == True:
        if int(body["searchCriteria"]) == 10:
            app.logger.info('Search Criteria 10 found! File Upload service has been detected.')
        else:
            app.logger.info('Loaded CDR/SMS found! Retrieving CDR/SMS data from cache.')
        body["searchCriteria"] = int(body["searchCriteria"])
        return cdrService.getCDR(body)

    # At this stage, we need to call backend.
    app.logger.info(f'Calling CDR data from backend')
    return callBackend(app, body, [])
