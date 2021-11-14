from src.services import graphDataService
from src.analyzedDataProvider import cdrUsageTypeFre
from src.analyzedDataProvider import mostVisitingArea
from src.analyzedDataProvider import msisdnListOnImei
from src.analyzedDataProvider import newNumberAfterDate
from src.analyzedDataProvider import timePeriodWiseUsageType
from src.analyzedDataProvider import imeiListOnMsisdn
from src.analyzedDataProvider import companySMS
from src.analyzedDataProvider import timePeriodWiseLoc
from src.analyzedDataProvider import locationSummaryProivider
from src.analyzedDataProvider import locationWithTime
from src.analyzedDataProvider import spendingTimeLoc
from src.analyzedDataProvider import partyBwithMaxMinDurTotal
from src.analyzedDataProvider import partyBwithMaxMinDur
from src.analyzedDataProvider import partyBwithMaxMinCdrCount
from src.analyzedDataProvider import datePeriodHeatMapProvider
from src.analyzedDataProvider import cdrMapPathDataProvider
from src.analyzedDataProvider import deviceInfoProvider
from src.multiValueSearchAnalyzer import imeiListOnMultiMsisdn
from src.multiValueSearchAnalyzer import msisdnListOnMultiImei
from src.multiValueSearchAnalyzer import timeWiseLocationforMultiValue
from src.analyzedDataProvider import dataAnalysis

from flask import Flask, Blueprint, current_app, request
import json

dataAnalysisBluePrint = Blueprint('dataAnalysisBluePrint', __name__,
                                  url_prefix="/query-service/api/v1/private/data-analysis")


@dataAnalysisBluePrint.route("summary", methods=['POST'])
def getAllAnalysis():
    """
    ---
    post:
      description: post for all analysis for list of request body (msisdn)
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: array
                items:
                    type: object
                    required:
                        - searchCriteria
                        - searchValues
                        - startDate
                        - endDate
                    properties:
                        searchCriteria:
                            type: string
                            description: MSISDN, IMEI
                        searchValues:
                            type:  array
                            items:
                                type: string
                        startDate:
                            type: string
                        endDate:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - data analysis for list of msisdn
    """
    
    return dataAnalysis.getResponse(request.json)


# 1-a
@dataAnalysisBluePrint.route("cdr/duration-wise-location/summary", methods=['POST'])
def getLocationWithduration():
    """
    ---
    post:
      description: Post for duration wise location. The response gives you locations with staying duration. Data should be presented by heatmap. Every location can also be shown in bar-chart. In bar-chart lac should be in x-axis and spentTimems should be in y-axis
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValues
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Duration wise location
    """
    
    return spendingTimeLoc.getResponse(request.json)


# 2-a
@dataAnalysisBluePrint.route("cdr/imei/msisdn-summary", methods=['POST'])
def getMultiPhoneNumberOnIMEI():
    """
    ---
    post:
      description: Post for MSISDNs used on given IMEI. Here you will get msisdns that were used in the given imei number with firstCdrTime and lastCdrTime. You can show this in table and  time slot graph. In time slot graph you can show msisdn, time starts with firstCdrTime and ends with lastCdrTime.
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description:  IMEI
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - MSISDNs with time
    """
    return msisdnListOnImei.getResponse(request.json)

# # 2-a multiple
# @dataAnalysisBluePrint.route("cdr/imei/multiple/msisdn-summary", methods=['POST'])
# def getMultiPhoneNumberOnMultipleIMEI():
#     """
#     ---
#     post:
#       description: Post for MSISDNs used on given list of IMEI. Here you will get msisdns that were used in the given imei number with firstCdrTime and lastCdrTime. You can show this in table and  time slot graph. In time slot graph you can show msisdn, time starts with firstCdrTime and ends with lastCdrTime.
#       requestBody:
#         required: true
#         content:
#           application/json:
#             schema:
#                 type: object
#                 required:
#                     - searchCriteria
#                     - searchValues
#                     - startDate
#                     - endDate
#                 properties:
#                     searchCriteria:
#                         type: string
#                         description:  IMEI
#                     searchValues:
#                         type:  array
#                         items:
#                             type: string
#                     startDate:
#                         type: string
#                     endDate:
#                         type: string
#       responses:
#         '200':
#           description: call successful
#       tags:
#           - MSISDNs with time for multi search-value
#     """
#     return msisdnListOnMultiImei.getResponse(request.json)



# 3-a
@dataAnalysisBluePrint.route("cdr/msisdn/imei-summary", methods=['POST'])
def getMultiIMEI():
    """
    ---
    post:
      description: Post for IMEI numbers used for given MSISDNs. Here you will get IMEI numbers that were used with the given msisdn with firstCdrTime and lastCdrTime. You can show this in table and  time slot graph. In time slot graph, you can show IMEI numbers, time starts with firstCdrTime and ends with lastCdrTime.
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValues
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - IMEI numbers on time
    """
    return imeiListOnMsisdn.getResponse(request.json)

# # 3-a-multiple
# @dataAnalysisBluePrint.route("cdr/msisdn/multiple/imei-summary", methods=['POST'])
# def getMultiIMEIForMultiMsisdn():
#     """
#     ---
#     post:
#       description: Post for IMEI numbers used for given list of MSISDNs. Here you will get IMEI numbers that were used with the given msisdns with firstCdrTime and lastCdrTime. You can show this in table and  time slot graph. In time slot graph, you can show IMEI numbers, time starts with firstCdrTime and ends with lastCdrTime.
#       requestBody:
#         required: true
#         content:
#           application/json:
#             schema:
#                 type: object
#                 required:
#                     - searchCriteria
#                     - searchValues
#                     - startDate
#                     - endDate
#                 properties:
#                     searchCriteria:
#                         type: string
#                         description: MSISDN
#                     searchValues:
#                         type:  array
#                         items:
#                             type: string
#                     startDate:
#                         type: string
#                     endDate:
#                         type: string
#       responses:
#         '200':
#           description: call successful
#       tags:
#           - IMEI numbers on time multi-search-value
#     """
#     return imeiListOnMultiMsisdn.getResponse(request.json)



# 4-a
@dataAnalysisBluePrint.route("cdr/time-wise-location/summary", methods=['POST'])
def getTimeWiseLocation():
    
    """
    ---
    post:
      description: Post for location analysis with time. Here you will get locations with firstCdrTime and lastCdrTime. You can show this in table and map with marker with the description and also can be shown in time slot graph where lac can be shown with start time that is firstCdrTime and end time that is lastCdrTime. 
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValues
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Locations with time
    """
    return locationWithTime.getResponse(request.json)


# # 4-a multi
# @dataAnalysisBluePrint.route("cdr/multiple/time-wise-location/summary", methods=['POST'])
# def getTimeWiseLocationForMultipleSearchValue():
    
#     """
#     ---
#     post:
#       description: Post for location analysis with time. Here you will get locations with firstCdrTime and lastCdrTime. You can show this in table and map with marker with the description and also can be shown in time slot graph where lac can be shown with start time that is firstCdrTime and end time that is lastCdrTime. 
#       requestBody:
#         required: true
#         content:
#           application/json:
#             schema:
#                 type: object
#                 required:
#                     - searchCriteria
#                     - searchValues
#                     - startDate
#                     - endDate
#                 properties:
#                     searchCriteria:
#                         type: string
#                         description: MSISDN, IMEI
#                     searchValues:
#                         type:  array
#                         items:
#                             type: string
#                     startDate:
#                         type: string
#                     endDate:
#                         type: string
#       responses:
#         '200':
#           description: call successful
#       tags:
#           - Locations with time for multiple search-values
#     """
#     return timeWiseLocationforMultiValue.getResponse(request.json)



# 5-a
@dataAnalysisBluePrint.route("cdr/usage-type/summary", methods=['POST'])
def getCDRUsagetypeHistory():
    """
    ---
    post:
      description: Post for usage-type analysis
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValues
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Usage-type count
    """
    return cdrUsageTypeFre.getResponse(request.json)


# 5-b
@dataAnalysisBluePrint.route("cdr/Bparty-with-max-and-min-duration/total", methods=['POST'])
def getMaxMinusageTypeTotalDuration():
    """
    ---
    post:
      description: Post for partyB that has maximum and minimum duration cdr(In total). Here you will get the list of partyB msisdn with whom given msisdn/imei has most cdr duration (key = partyBWithMaxDuration), list of partyB with whom given msisdn/imei has least cdr duration (key = partyBWithMinDuration), list of partyBs that has most and least MOC (key = moc), list of partyBs that has most and least MTC (key = MTC)
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Bparties with max-min total duration 
    """

    return partyBwithMaxMinDurTotal.getResponse(request.json)


# 5-c
@dataAnalysisBluePrint.route("cdr/Bparty-with-max-and-min-duration", methods=['POST'])
def getMaxMinusageTypeDuration():
    """
    ---
    post:
      description: Post for partyB that has maximum and minimum duration cdr. Here you will get the list of partyB msisdn with whom given msisdn/imei has most total cdr duration (key = partyBWithMaxDuration), list of partyB with whom given msisdn/imei has least cdr duration (key = partyBWithMinDuration), list of partyBs that has most and least MOC (key = moc), list of partyBs that has most and least MTC (key = MTC)
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Bparties with max-min duration
    """

    return partyBwithMaxMinDur.getResponse(request.json)


# 5-d
@dataAnalysisBluePrint.route("cdr/Bparty-with-max-and-min-cdr-count", methods=['POST'])
def getMaxMinusageTypeCount():
    """
    ---
    post:
      description: Post for partyB that has maximum and minimum cdr count. Here you will get the list of partyB msisdn with whom given msisdn/imei has most cdr count (key = partyBWithMaxCount), list of partyB with whom given msisdn/imei has least cdr duration (key = partyBWithMinCount), list of partyBs that has most and least MOC (key = moc), list of partyBs that has most and least MTC (key = MTC)
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Bparties with max-min cdr-count
    """

    return partyBwithMaxMinCdrCount.getResponse(request.json)




# 6-a
@dataAnalysisBluePrint.route("cdr/time-period-wise-location/summary", methods=['POST'])
def getPeriodWiseLocation():
    """
    ---
    post:
      description: Post for time period wise locations analysis. This will give you locations in  night, lateNight, earlyMorning, morning, noon, evening. In every section you will get list of data where given lac,latitude, longitude, firstCdrTime and lastCdrTime. 
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Time period wise locations
    """
    return timePeriodWiseLoc.getResponse(request.json)


# 6-b box heat map
@dataAnalysisBluePrint.route("cdr/date-time-period-heat-map/summary", methods=['POST'])
def getDateAndPeriodWiseSummary():
    """
    ---
    post:
      description: Post for time period wise locations analysis. This will give you locations in  night, lateNight, earlyMorning, morning, noon, evening. In every section you will get list of data where given lac,latitude, longitude, firstCdrTime and lastCdrTime. 
      parameters:
        - in: query
          name: by
          schema:
            type: long
          description: cdr-count/total-duration


      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Heat Map Data date in x-axis and time period in y-axis
    """
    generateBy =request.args.get('by')

    return datePeriodHeatMapProvider.getResponse(request.json, generateBy)



# 7-a
@dataAnalysisBluePrint.route("cdr/time-period-wise-usage-type/summary", methods=['POST'])
def getTimePeriodWiseCallSummary():
    """
    ---
    post:
      description: Post for time period wise locations analysis. This will give you msisdns with their moc, mtc, smsmt and smsmo count in  night, lateNight, earlyMorning, morning, noon, evening. In every section you will get list of data where given partyB msisdn with their moc, mtc, smsmt, smsmo. 
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValues
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN, IMEI
                    searchValues:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Time period wise usage-type
    """
    return timePeriodWiseUsageType.getResponse(request.json)


# 9-a
@dataAnalysisBluePrint.route("msisdn/company-sms", methods=['POST'])
def getCompanySms():
    """
    ---
    post:
      description: Post for company sms, Here you will get list of data. In every data you will get sender, sedingTime and smsContent. Data can be shown in table.
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - Company SMS
    """
    return companySMS.getResponse(request.json)


# 10-a
@dataAnalysisBluePrint.route("cdr/map/path", methods=['POST'])
def getMapPathData():
    """
    ---
    post:
      description: Post for path data on map
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - map path data
    """
    return cdrMapPathDataProvider.getResponse(request.json)

# 11
@dataAnalysisBluePrint.route("cdr/device-information", methods=['POST'])
def getDeviceInformation():
    """
    ---
    post:
      description: Post for device information
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - searchCriteria
                    - searchValue
                    
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN
                    searchValue:
                        type: string
                    
      responses:
        '200':
          description: call successful
      tags:
          - Device Information
    """
    return deviceInfoProvider.getResponse(request.json)


# @dataAnalysisBluePrint.route("cdr/msisdn/summary", methods=['POST'])
# def getMsisdnSummary():
#     return graphDataService.getData(current_app, request.json)


# @dataAnalysisBluePrint.route("cdr/imei/summary", methods=['POST'])
# def getImeiSummary():
#     return graphDataService.getData(current_app, request.json)


# @dataAnalysisBluePrint.route("cdr/location/summary/", methods=['POST'])
# def getLocationHistory():
#     return locationSummaryProivider.getLocationSummary(current_app, request.json)


# @dataAnalysisBluePrint.route("cdr/visiting-area/summary", methods=['POST'])
# def getFrequentVisitingArea():
#     return mostVisitingArea.getData(current_app, request.json)


# @dataAnalysisBluePrint.route("cdr/location-with-most-time/summary", methods=['POST'])
# def getLocationOfMostSpending():
#     return json.dumps(locationWithTime.getData(current_app, request.json))


# @dataAnalysisBluePrint.route("cdr/new-numbers-after", methods=['POST'])
# def getNewNumbersOnIMEI():
#     # return  json.dumps(newNumberAfterDate.getData(current_app, request.json), indent=4)
#     return newNumberAfterDate.getData(current_app, request.json)
