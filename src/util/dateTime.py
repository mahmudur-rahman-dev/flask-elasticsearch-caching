from datetime import datetime
import pytz

def convertToYearMonthDay(date):
    return datetime.fromtimestamp(int(date), pytz.timezone("Asia/Dhaka")).strftime("%Y%m%d%H%M%S")

def convertEsDob(date):
    return (datetime.strptime(date,"%Y%m%d")).strftime("%Y-%m-%d")

def getCurrentTimestampMS():
    currentTime =  round(datetime.utcnow().timestamp() * 1000)
    return currentTime