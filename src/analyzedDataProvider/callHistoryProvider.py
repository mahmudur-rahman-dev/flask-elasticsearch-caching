from . import cdrUsageTypeFre
from . import multiIMEI
from . import companySMS
from . import nightCallsSummary
import json

def getCallHistory(app, body):
    
    callSummary = {
        "usageTypeHistory" : cdrUsageTypeFre.getData(app, body),
        "nightCalls" : nightCallsSummary.getData(app,body)
        "usedInImei" : multiIMEI.getData(app, body),
        "companySMSHistory" : companySMS.getData(app, body)
    }
 
    return json.dumps(callSummary, indent = 4) 

