def getEmptyResponse(index):
    response = {
        "data": {
            "numberOfRecords": 0,
            "responseRecords": []
        },
        "error": None,
        "type": get_type(index)
    }
    return response

def get_type(index):
    if index == "esaf":
        return "ESAF"
    elif index == "passport":
        return "PASSPORT"
    elif index == "driving-license":
        return "DRIVINGLICENSE"
    elif index == "birth_registration":
        return "BIRTHREGISTRATION"
