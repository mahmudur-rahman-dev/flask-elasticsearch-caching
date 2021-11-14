
def getOperator(body):
    if body['searchValue'].startswith('88017') or body['searchValue'].startswith('017') or body['searchValue'].startswith('013') or body['searchValue'].startswith('88013'):
        return "GP"
    elif body['searchValue'].startswith('88019') or body['searchValue'].startswith('019') or body['searchValue'].startswith('88014') or body['searchValue'].startswith('014'):
        return "BL"
    elif body['searchValue'].startswith('88018') or body['searchValue'].startswith('88016') or \
            body['searchValue'].startswith('018') or body['searchValue'].startswith('016'):
        return "RB"
    elif body['searchValue'].startswith('88015') or body['searchValue'].startswith('015'):
        return "TT"
    else:
        return ""
def getCdrResponse(body,cdrData):
    responseBody = {
        "data": {
            "mnoRequestType": "CDR",
            "numberofRecordsFound": 0,
            "responseRecord": []
        },
        "error":None,
        "type":"CDR",
        "operator":getOperator(body)
    }
    for esdata in cdrData:
        data = esdata['_source']
        responseRecord = {
            'responseId': data['response_id'] if 'response_id' in data else '',
            'partyA': data['party_a'] if 'party_a' in data else '',
            'partyB': data['party_b'] if 'party_b' in data else '',
            'eventTime': data['event_time'] if 'event_time' in data else '',
            'callDuration': data['call_duration'] if 'call_duration' in data else '',
            'usageType': data['usage_type'] if 'usage_type' in data else '',
            'cellType': data['cell_type'] if 'cell_type' in data else '',
            'imeiNumber': data['imei_number'] if 'imei_number' in data else '',
            'btsName': data['bts_name'] if 'bts_name' in data else '',
            'mccStartA': data['mcc_start_a'] if 'mcc_start_a' in data else '',
            'mncStartA': data['mnc_start_a'] if 'mnc_start_a' in data else '',
            'lacStartA': data['lac_start_a'] if 'lac_start_a' in data else '',
            'ciStartA': data['ci_start_a'] if 'ci_start_a' in data else '',
            'providerName': data['provider_name'] if 'provider_name' in data else '',
            'imsi': data['imsi'] if 'nid' in data else '',
            'timeStamp': data['time_stamp'] if 'time_stamp' in data else '',
            'operator': data['operator'] if 'operator' in data else '',
            'partybOriginal': data['partyb_original'] if 'partyb_original' in data else ''
        }
        responseBody['data']['responseRecord'].append(responseRecord)
    responseBody['data']['numberofRecordsFound'] = len(cdrData)
    return responseBody

def getNoDataFoundCdrResponse(body):
    responseBody = {
        "data": {
            "mnoRequestType": "CDR",
            "numberofRecordsFound": 0,
            "responseRecord": []
        },
        "error":None,
        "type":"CDR",
        "operator":getOperator(body)
    }
