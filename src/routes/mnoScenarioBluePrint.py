from flask import Flask, Blueprint, current_app, request
from src.services import dateRangeService
from src.services import esafService
from src.services import nidService
from src.responseBuilder import errorResponseBuilder;

mnoScenarioBluePrint  = Blueprint('mnoScenarioBluePrint ', __name__,
                         url_prefix="/query-service/api/v1/private/scenario/search-data")

@mnoScenarioBluePrint .route('/test', methods=['GET'])
def test():
  print("testing")
  return "okkkk"

@mnoScenarioBluePrint .route('/cdr', methods=['POST'])
def callCDRService():
    """
    ---
    post:
      description: Post to CDR
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - requestType
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                    - channels
                properties:
                    requestType:
                        type: string
                        description: CDR,ESAF,SMS,NID..
                    searchCriteria:
                        type: integer
                        description: 1,2,3,4..
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - CDR
    """
    print("Excuting callCDRService")
    return dateRangeService.dateRangeServices(request.json)


@mnoScenarioBluePrint .route('/sms', methods=['POST'])
def callSMSService():
    """
    ---
    post:
      description: Post to SMS
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - requestType
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                    - channels
                properties:
                    requestType:
                        type: string
                        description: CDR,ESAF,SMS,NID..
                    searchCriteria:
                        type: integer
                        description: 1,2,3,4..
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - SMS
    """
    print("Excuting callSMSService")
    return dateRangeService.dateRangeServices(request.json)


@mnoScenarioBluePrint .route('/esaf', methods=['POST'])
def callESAFService():
    """
    ---
    post:
      description: Post to ESAF
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - requestType
                    - searchCriteria
                    - searchValue
                    - startDate
                    - endDate
                    - channels
                properties:
                    requestType:
                        type: string
                        description: CDR,ESAF,SMS,NID..
                    searchCriteria:
                        type: integer
                        description: 1,2,3,4..
                    searchValue:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - ESAF
    """
    print("Excuting callESAFService")
    return esafService.getESAF(request.json)
