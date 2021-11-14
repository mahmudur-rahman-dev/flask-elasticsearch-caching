from flask import Flask, Blueprint, current_app, request
from src.services import dateRangeService
from src.services import esafService
from src.services import nidService
from src.services import deviceInfoService

mnoBluePrint = Blueprint('mnoBluePrint', __name__,
                         url_prefix="/query-service/api/v1/private/discovery/search-data")


@mnoBluePrint.route('/cdr', methods=['POST'])
def callCDRService():
    """
    ---
    post:
      description: Post to CDR
      parameters:
        - in: path
          name: caseId   # Note the name is the same as in the path
          required: true
          schema:
            type: integer
          description: The case ID

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
    app = current_app
    app.logger.info(f'Arrived at mnoBluePrint CDR POST call with: {request.json}')
    return dateRangeService.dateRangeServices(request.json)


@mnoBluePrint.route('/sms', methods=['POST'])
def callSMSService():
    """
    ---
    post:
      description: Post to SMS
      parameters:
        - in: path
          name: caseId   # Note the name is the same as in the path
          required: true
          schema:
            type: integer
          description: The case ID
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
    app = current_app
    app.logger.info(f'Arrived at mnoBluePrint SMS POST call with: {request.json}')
    return dateRangeService.dateRangeServices(request.json)


@mnoBluePrint.route('/esaf', methods=['POST'])
def callESAFService():
    """
    ---
    post:
      description: Post to ESAF
      parameters:
        - in: path
          name: caseId   # Note the name is the same as in the path
          required: true
          schema:
            type: integer
          description: The case ID
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
    return esafService.getESAF(request.json)



@mnoBluePrint.route('/device-information', methods=['POST'])
def callDeviceInfoService():
    """
    ---
    post:
      description: Post to device-information
      parameters:
        - in: path
          name: caseId   # Note the name is the same as in the path
          required: true
          schema:
            type: integer
          description: The case ID
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
                    - channels
                properties:
                    requestType:
                        type: string
                        description: MOBILE_DEVICE_INFORMATION,CDR,ESAF,SMS,NID..
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
    current_app.logger.info(f"request for device-info: {request.json}")
    return deviceInfoService.getDeviceInformation(request.json)

    
