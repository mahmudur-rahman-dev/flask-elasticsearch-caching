from flask import Flask, Blueprint, current_app, request
from src.dbService import esService
from src.util import esRequestBodyGenerator
from src.responseBuilder import esafResponseBuilder, passportResponseBuilder, drivingLicenseResponseBuilder, birthRegResponseBuilder, nidResponseBuilder, emptyResponseBuilder

elasticSearchQueryBluePrint = Blueprint('elasticSearchQueryBluePrint', __name__,
                         url_prefix="/query-service/api/v1/private/search")

@elasticSearchQueryBluePrint.route('/<string:index>/<string:value>', methods=['GET'])
def fetchDataFromES(index, value):
    request_body = esRequestBodyGenerator.generate(index, value)
    index = process(index)
    esResponse = esService.search(index, request_body)
    return buildResponse(esResponse, index)

def process(index):
    nid_indices = ["nid10Digit", "nid13Digit", "nid17Digit"]
    if index in nid_indices:
        return "nid"
    return index

def buildResponse(esResponse, index):
    if index == "esaf":
        return esafResponseBuilder.getEsafResponse(None, esResponse)
    elif index == "passport":
        return passportResponseBuilder.getPassportResponse(esResponse)
    elif index == "driving-license":
        return drivingLicenseResponseBuilder.getDrivingLicenseResponse(esResponse)
    elif index == "birth_registration":
        return birthRegResponseBuilder.getBirthRegResponse(esResponse)
    elif index == "nid":
        return nidResponseBuilder.getNidResponse(esResponse)
    return None