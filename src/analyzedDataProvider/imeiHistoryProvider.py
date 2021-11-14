from . import multiPhnOnImei
from . import multiIMEI
from . import companySMS
from . import nightCallsSummary
import json

def getCallHistory(app, body):
    
    IMEISummary = {
        "usedMSISDN" : multiPhnOnImei.getData(app, body),
        "mostVisitedArea" : mostVisitingArea.getData(app, body),
        "nightRestingArea" : nightRestingArea.getData(app, body)
    }
 
    return json.dumps(IMEISummary, indent = 4) 
