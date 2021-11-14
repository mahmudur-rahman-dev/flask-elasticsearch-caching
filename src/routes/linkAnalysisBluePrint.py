
from flask import Flask, Blueprint, current_app as app, request

from src.linkAnalyzer import sourceMnoLinkAnalizer
from src.linkAnalyzer import generateLinkAnalysisGraph
from src.linkAnalyzer import nodeInfo
from src.linkAnalyzer import edgeInfo
from src.linkAnalyzer import initiateCdr
from src.linkAnalyzer import linkAnalysisForMultiMsisdn
from src.linkAnalyzer import multipleCdrIntitiate

linkAnalysisBluePrint = Blueprint('linkAnalysisBluePrint', __name__,
                           url_prefix="/query-service/api/v1/private/link-analysis")



# @linkAnalysisBluePrint.route("cdr/source-msisdn", methods=['POST'])
# def getlinkAnalysis():
#     """
#     ---
#     post:
#       description: post for link analysis data for source msisdn
#       requestBody:
#         required: true
#         content:
#           application/json:
#             schema:
#                 type: object
#                 required:
#                     - searchCriteria
#                     - searchValue
#                     - startDate
#                     - endDate
#                     - noOfLinks
#                 properties:
#                     searchCriteria:
#                         type: string
#                         description: MSISDN
#                     searchValue:
#                         type: array
#                         items:
#                             type: string
#                     startDate:
#                         type: string
#                     endDate:
#                         type: string
#                     noOfLinks:
#                         type: integer
#       responses:
#         '200':
#          description: call successful
#       tags:
#           - Link analysis of source msisdn
#     """
#     app.logger.info(request.json)

#     return sourceMnoLinkAnalizer.getResponse(request.json)


@linkAnalysisBluePrint.route("/mno/cdr/multiple", methods=['POST'])
def getGraphDataForMultiMsisdn():

    """
    ---
    post:
      description: post for link analysis graph data for multiple request-body
      parameters:
        - in: query
          name: by
          schema:
            type: long
          description: call-count/sms-count/call-duration

      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: array
                items : 
                    type: object
                    required:
                        - searchMode
                        - msisdns
                        - startDate
                        - endDate
                        - noOfLinks
                    properties:    
                        searchMode:
                            type: string
                            description: LINK_ANALYSIS_VIEW
                        msisdns:
                            type: array
                            items:
                                type: string
                        startDate:
                            type: string
                        endDate:
                            type: string
                        noOfLinks:
                            type: integer
                        
      responses:
        '200':
          description: call successful
      tags:
          - Link analysis of msisdns
                    
                
    """

    generateBy =request.args.get('by')

    return linkAnalysisForMultiMsisdn.getResponse(request.json, generateBy)


@linkAnalysisBluePrint.route("initiate", methods=['POST'])
def initiateCDR():
    """
    ---
    post:
      description: post for cdrs data for multiple msisdn
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - caseId
                    - agencyId
                    - userId
                    - msisdns
                    - startDate
                    - endDate
                    - channels
                properties:
                    caseId:
                        type: string
                    agencyId:
                        type: string
                    userId:
                        type: string
                    msisdns:
                        type:  array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
                    noOfLinks:
                        type: integer
                    channels:
                        type: array
                        items:
                            type: string
      responses:
        '200':
          description: call successful
      tags:
          - cdr call for multiple msisdn
    """
    app.logger.info(request.json)

    return initiateCdr.callBackendForCdr(request.json)


@linkAnalysisBluePrint.route("cdr/multiple/initiate", methods=['POST'])
def initiateCDRForMultipleRequest():
    """
    ---
    post:
      description: post for cdrs data for list of request-body
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: array
                items: 
                    type: object
                    required:
                        - caseId
                        - agencyId
                        - userId
                        - msisdns
                        - startDate
                        - endDate
                        - channels
                    properties:
                        caseId:
                            type: string
                        agencyId:
                            type: string
                        userId:
                            type: string
                        msisdns:
                            type:  array
                            items:
                                type: string
                        startDate:
                            type: string
                        endDate:
                            type: string
                        noOfLinks:
                            type: integer
                        channels:
                            type: array
                            items:
                                type: string
      responses:
        '200':
          description: call successful
      tags:
          - cdr call for multiple msisdn
    """
    app.logger.info(request.json)

    return multipleCdrIntitiate.getResponse(request.json)





@linkAnalysisBluePrint.route("mno/cdr", methods=['POST'])
def generateGraph():
    """
    ---
    post:
      description: post for link analysis graph data 
      parameters:
        - in: query
          name: by
          schema:
            type: long
          description: call-count/sms-count/call-duration

      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    # - caseId
                    # - agencyId
                    # - userId
                    - searchMode
                    - msisdns
                    - startDate
                    - endDate
                    - noOfLinks
                properties:
                    
                    # caseId:
                    #     type: string
                    # agencyId:
                    #     type: string
                    # userId:
                    #     type: string
                    searchMode:
                        type: string
                        description: LINK_ANALYSIS_VIEW
                    searchValue:
                        type: array
                        items:
                            type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
                    noOfLinks:
                        type: integer
                    
      responses:
        '200':
          description: call successful
      tags:
          - Link analysis of msisdns
    """
    generateBy =request.args.get('by')
    app.logger.info(request.json)
    app.logger.info(f"generate graph by- {generateBy}")

    return generateLinkAnalysisGraph.getResponse(body = request.json, generateBy=generateBy)


@linkAnalysisBluePrint.route("cdr/msisdn-info", methods=['POST'])
def getNodeInfo():
    """
    ---
    post:
      description: post for data for a msisdn node
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
          - PartyB usgae-type information for an edge 
    """
    return nodeInfo.getResponse(request.json)



@linkAnalysisBluePrint.route("cdr/edge-info", methods=['POST'])
def getEdgeInfo():

    """
    ---
    post:
      description: post for cdr information between two node (of an edge)
      requestBody:
        required: true
        content:
          application/json:
            schema:
                type: object
                required:
                    - partyA
                    - partyB
                    - startDate
                    - endDate
                properties:
                    searchCriteria:
                        type: string
                        description: MSISDN
                    partyA:
                        type: string
                    partyB:
                        type: string
                    startDate:
                        type: string
                    endDate:
                        type: string
      responses:
        '200':
          description: call successful
      tags:
          - PartyB usgae-type information for a node 
    """

    return edgeInfo.getResponse(request.json)


