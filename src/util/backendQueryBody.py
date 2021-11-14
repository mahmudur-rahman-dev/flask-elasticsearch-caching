from src.constant import constant
def getBody(body):

    newBody = {
        "msisdn": body["searchValue"],
        "requestData": body["requestType"].upper(),
        "selectionCriteria": body["searchCriteria"],
        "startDate": body['startDate'] if 'startDate' in body else '' ,
        "endDate": body['endDate'] if 'endDate' in body else '',
        "channels": body['channels'],
        "searchMode" : body["searchMode"],
        "caseId" : body["caseId"],
        "agencyId" : body["agencyId"],
        "userId" : body["userId"],
        "discoveryId": body["discoveryId"] if 'discoveryId' in body else None,
        "unifiedViewerBase": body['unifiedViewerBase'] if 'unifiedViewerBase' in body else False,
        "unifiedViewerId": body["unifiedViewerId"] if 'unifiedViewerId' in body else None,
        "additionalSearchParams": body["additionalSearchParams"] if 'additionalSearchParams' in body else None
    }
    # newBody = 0
    return newBody
