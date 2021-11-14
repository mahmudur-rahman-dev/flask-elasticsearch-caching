from src.constant.constant import getSearchedWith,requestTypeId
import requests
from flask import current_app as app

def getDipUnifiedViewerSearchSummary(body, responseType):
    return {
        "userId": body['userId'],
        "agencyId": body['agencyId'],
        "caseId": body['caseId'],
        "discoveryId": body['discoveryId'],
        "unifiedViewerId": body['unifiedViewerId'],
        "dipSearchCriteriaId": body['selectionCriteria'],
        "searchValue": getSearchedWith(body, responseType),
        "dipRequestTypeId": requestTypeId[responseType],
        "unifiedViewerBase": body['unifiedViewerBase'] if 'unifiedViewerBase' in body else False,
        "additionalSearchParams": body["additionalSearchParams"] if 'additionalSearchParams' in body else None,
        "resultStatus": 1
    }

def insertDataToDipUnifiedViewerSearchSummary(body, responseType):
    unifiedViewerSearchSummary = getDipUnifiedViewerSearchSummary(body, responseType)
    headers = {'Content-type': 'application/json'}
    url = f"{app.config['CASE_MANAGEMENT_HOST']}{app.config['CASE_MANAGEMENT_UNIFIED_VIEWER_CREATION_URL']}"
    try:
        requests.post(url=url, json=unifiedViewerSearchSummary,headers=headers)
    except:
        app.logger.exception("Error while post to Case Management")

