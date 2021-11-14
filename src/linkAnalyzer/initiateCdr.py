from src.services import dateRangeService



def callBackendForCdr(body):
    backendBody=body.copy()
    backendBody['searchCriteria'] = 1
    backendBody['requestType'] = 'CDR'
    backendBody['searchMode'] = 'LINK_ANALYSIS_VIEW'
    

    if(len(body['msisdns']) > 0):
        for value in body['msisdns']:
            backendBody['searchValue'] = value
            dateRangeService.dateRangeServices(backendBody)
            
    return "posted for cdr to backend"
    
