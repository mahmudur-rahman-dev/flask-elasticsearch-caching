from datetime import datetime
def getErrorResponse(body, error):
    response = {
        "data": None,
        "error": {
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "status": "INTERNAL_SERVER_ERROR",
            "error": "",
            "message": "Request Failed"
        },
        "type": body['requestType'].upper() if 'requestType' in body else ""
    }
    for errorMessage in error.args:
        response["error"]["error"] +=  f"{str(errorMessage)} | "
    return response
