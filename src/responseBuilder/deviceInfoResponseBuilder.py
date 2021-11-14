
from src.util import dateTime

def getDeviceInfoResponse(body, deviceInfoData):
    responseBody = {
        "data": {
            "mnoRequestType": "MOBILE_DEVICE_INFORMATION"
        },
        "error": None,
        "type": "MOBILE_DEVICE_INFORMATION"
    }

    # for esdata in esafData:
    #     data = esdata['_source']
    #     responseRecord = {
    #         "responseId": data["responseId"] if 'responseId' in data else '',
    #         "address": data["address"] if 'address' in data else '',
    #         "phone": data["phone"] if 'phone' in data else '',
    #         "nid": data["nid"] if 'nid' in data else '',
    #         "name": data["name"] if 'name' in data else '',
    #         "birthDate": dateTime.convertEsDob(data["birth_date"]) if 'birth_date' in data else '',
    #         "operator": data["operator"] if 'operator' in data else ''
    #     }
    #     responseBody["data"]["responseRecord"].append(responseRecord)
    responseBody["data"] = deviceInfoData
    return responseBody
    
