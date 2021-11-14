def getSMSResponse(body, smsData):
    responseBody = {
        "data": {
            "mnoRequestType": "SMS",
            "numberofRecordsFound": 0,
            "responseRecord": [],
        },
        "error": None,
        "type": "SMS",
    }
    for esdata in smsData:
        data = esdata['_source']
        responseRecord = {
            "responseId": data["response_id"] if 'response_id' in data else '',
            "partyA": data["party_a"] if 'party_a' in data else '',
            "partyB": data["party_b"] if 'party_b' in data else '',
            "eventTime": data["event_time"] if 'event_time' in data else '',
            "timeStamp": data["time_stamp"] if 'time_stamp' in data else '',
            "direction": data["direction"] if 'direction' in data else '',
            "content": data["content"] if 'content' in data else '',
            "textFormat": data["text_format"] if 'text_format' in data else '',
            "partyBOriginal": data["partyb_original"] if 'partyb_original' in data else ''
            # "operator": data["operator"]
        }
        responseBody["data"]["responseRecord"].append(responseRecord)
    responseBody["data"]["numberofRecordsFound"] = len(smsData)
    return responseBody
