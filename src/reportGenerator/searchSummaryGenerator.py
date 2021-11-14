from src.util import dateTime
from src.dbService import esService as es
from src.constant import constant
import uuid
from flask import current_app as app


def saveSearchSummary( body,response, searchedAt, status, requestType):

    documents = createDocument(body,response, searchedAt, status, requestType)
    response = insertData(documents)
    app.logger.info(f"response from es after saving search-summary-log : {response}")

def insertData(docs):
    res = es.insert("search-summary-log", docs)
    return res
    
   

def createDocument(body,response, searchedAt, status, requestType):

    body['searchedWith'] = constant.getSearchedWith(body=body, type=requestType)

    document = {

        'search_summary_uuid' : uuid.uuid1(),
        'searched_at' : searchedAt,
        'search_mode' : body['searchMode'] if 'searchMode' in body else None,
        'case_id' : body['caseId'],
        'agency_id' : body['agencyId'],
        'user_id' : body['userId'],
        'request_type' : requestType,
        'selection_criteria' : getSelectionCriteria(body),
        'searched_value' : body,
        'from_cache' : 1,
        'data_retrieval_status' : 'SUCCESS' if status==True else 'FAILURE',
        'start_date' : body['startDate'] if 'startDate' in body else None,
        'end_date' : body['endDate'] if 'endDate' in body else None,
        'response' : response,
        'responded_at' : dateTime.getCurrentTimestampMS(),
        'discovery_id' : body['discoveryId'] if 'discoveryId' in body else None,
        'unified_viewer_base' : body['unifiedViewerBase'] if 'unifiedViewerBase' in body else None

    }

    return document

def getSelectionCriteria(body):
    app.logger.info(f"{type(body)}  {body.keys()}")
    if 'selectionCriteria' in body.keys() :
         return body['selectionCriteria']
    else:
          return None
    return None

