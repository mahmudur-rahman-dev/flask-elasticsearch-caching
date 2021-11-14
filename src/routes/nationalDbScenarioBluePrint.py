from flask import Flask, Blueprint, current_app, request
from src.services import passportService
from src.services import vehicleRegService
from src.services import drivingLicenseService
from src.services import birthRegService
from src.services import nidService
nationalDbScenarioBluePrint  = Blueprint(
    'nationalDbScenarioBluePrint ', __name__, url_prefix="/query-service/api/v1/private/scenario/search-data")


@nationalDbScenarioBluePrint .route('/nid', methods=['POST'])
def callNIDService():
    """
    ---
    post:
      description: Post to NID
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - nidNumber
                    - dateOfBirth
                    - channels
                properties:
                    nidNumber:
                        type: string
                    dateOfBirth:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
        - NID
    """
    print("Exceuting callNIDService")
    return nidService.getNid(request.json)


@nationalDbScenarioBluePrint .route('/passport', methods=['POST'])
def callPassportService():
    """
    ---
    post:
      description: Post to Passport
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - parameterType
                    - parameterValue
                    - channels
                properties:
                    parameterType:
                        type: string
                    parameterValue:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - Passport
    """
    print("Exceuting callPassportService")
    return passportService.getPassport(request.json)


@nationalDbScenarioBluePrint .route('/driving-license', methods=['POST'])
def callDrivingLicenseService():
    """
    ---
    post:
      description: Post to Driving License
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - parameterType
                    - parameterValue
                    - channels
                properties:
                    parameterType:
                        type: string
                    parameterValue:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - Driving License
    """
    print("Exceuting callDrivingLicenseService")
    return drivingLicenseService.getDrivingLicense(request.json)


@nationalDbScenarioBluePrint .route('/vehicle-registration', methods=['POST'])
def callVehicleRegistrationService():
    """
    ---
    post:
      description: Post to Vehicle Registration
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - zone
                    - series
                    - vehicleNumber
                    - channels
                properties:
                    zone:
                        type: string
                    vehicleNumber:
                        type: string
                    series:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - Vehicle Registration
    """
    print("Exceuting callVehicleRegistrationService")
    return vehicleRegService.getVehicleRegistration(request.json)


@nationalDbScenarioBluePrint .route('/birth-registration', methods=['POST'])
def callBirthRegistrationService():
    """
    ---
    post:
      description: Post to Birth Registration
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - birthRegNo
                    - birthDate
                    - channels
                properties:
                    birthRegNo:
                        type: string
                    birthDate:
                        type: string
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - Birth Registration
    """
    print("Exceuting callBirthRegistrationService")
    return birthRegService.getBirthRegistration(request.json)
