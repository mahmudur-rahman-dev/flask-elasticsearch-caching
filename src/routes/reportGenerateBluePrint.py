from flask import Flask, Blueprint, current_app as app, request, send_from_directory, send_file, render_template

from src.reportGenerator import agencyReport
from src.reportGenerator import userReport
from src.reportGenerator import singleAgencyReport
from src.reportGenerator import singleUserReport
from src.reportGenerator import requestTypeReport
from src.reportGenerator import agencyRequestTypeReport
from src.reportGenerator import userQueryStatusReport
# from flask import current_app as app

# import pdfkit
# import os

reportGenerateBluePrint = Blueprint(
    'reportGenerateBluePrint', __name__, url_prefix="/query-service/api/v1/private/report/")


# options = {
#     'page-size': 'A3',
#     'margin-top': '0.75in',
#     'margin-right': '0.75in',
#     'margin-bottom': '0.75in',
#     'margin-left': '0.75in',
#     'encoding': "UTF-8",
#     'custom-header' : [
#         ('Accept-Encoding', 'gzip')
#     ],
#     'cookie': [
#         ('cookie-name1', 'cookie-value1'),
#         ('cookie-name2', 'cookie-value2'),
#     ],
#     'no-outline': None
# }

@reportGenerateBluePrint.route("agencies", methods=['GET'])
def getAgencyReport():

    """
    ---
    get:
      summary: Returns all agency request informations.
      parameters:
        
        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
      tags:
        - All agency's request information

    """
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate') 
    print(type(startDate), type(endDate))
    return agencyReport.getResponse(startDate, endDate)
    

@reportGenerateBluePrint.route("users", methods=['GET'])
def getUserReport(): 

    """
    ---
    get:
      summary: Returns all user's request informationof an agency. If no agency specified then returns users of all agencies.
      parameters:
        
        - in: query
          name: agency
          schema:
            type: string
          description: Agency Id

        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
               
      tags:
        - All user's request information

    """
    agencyId = request.args.get('agency')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate') 
    app.logger.info(f'request: {agencyId}, {startDate}, {endDate}')
    return userReport.getResponse(agencyId=agencyId, startDate=startDate, endDate=endDate)

@reportGenerateBluePrint.route("agency/<agencyId>/request-summary", methods=['GET'])
def getAgencyIDReport(agencyId): 
    
    """
    ---
    get:
      summary: Returns an agency request information by ID.
      parameters:
        - in: path
          name: agencyId
          required: true
          type: string

        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
                
      tags:
        - Single agency request information

    """

    print("agency report: ", agencyId)
    startTime =request.args.get('startDate')
    endTime = request.args.get('endDate')
    return singleAgencyReport.getResponse(agencyId=agencyId, startTime=startTime,endTime= endTime)

    

@reportGenerateBluePrint.route("user/<userId>/request-summary", methods=['GET'])
def getUserIdReport(userId): 
    
    """
    ---
    get:
      summary: Returns a user request information by ID.
      parameters:
        - in: path
          name: userId
          required: true
          type: uuid
          description: user uuid


        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
      tags:
        - Single user request information

    """

    print("user report: ", userId)
    startTime =request.args.get('startDate')
    endTime = request.args.get('endDate')

    return singleUserReport.getResponse(userId=userId, startTime=startTime, endTime=endTime)



@reportGenerateBluePrint.route("request-type/<requestType>/request-summary", methods=['GET'])
def getRequestTypeReport(requestType): 
    
    """
    ---
    get:
      summary: Returns request information by requestType for all agencies.
      parameters:
        - in: path
          name: requestType
          required: true
          type: String
          description: request type in capital letter


        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
                
      tags:
        - Request-type wise information for all agencies

    """

    print("request-type report: ", requestType)
    startTime =request.args.get('startDate')
    endTime = request.args.get('endDate')

    return requestTypeReport.getResponse(requestType=requestType, startTime=startTime, endTime=endTime)


@reportGenerateBluePrint.route("request-type/<requestType>/agency/<agencyId>/request-summary", methods=['GET'])
def getRequestTypeReportForAgency(requestType, agencyId): 
    
    """
    ---
    get:
      summary: Returns request information by requestType for all users of single agency.
      parameters:
        - in: path
          name: requestType
          required: true
          type: string
          description: CDR, ESAF, SMS, LRL, NID, PASSPORT, DRIVINGLICENSE, VEHICLEREGISTRATION, BIRTHREGISTRATION, 
        
        - in: path
          name: agencyId
          required: true
          type: string
          description: agency ID


        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
                
      tags:
        - Request-type wise information for single agency

    """

    print("request-type report: ", requestType, agencyId)
    startTime =request.args.get('startDate')
    endTime = request.args.get('endDate')

    return agencyRequestTypeReport.getResponse(requestType=requestType,agencyId=agencyId, startTime=startTime, endTime=endTime)




@reportGenerateBluePrint.route("request-type/query-status/user/<userId>", methods=['GET'])
def getQueryStatusForUser(userId): 
    
    """
    ---
    get:
      summary: Returns query-status by requestType and their provider for single user
      parameters:
        - in: path
          name: userId
          required: true
          type: string

        - in: query
          name: startDate
          schema:
            type: long
          description: time in milisecond

        - in: query
          name: endDate
          schema:
            type: long
          description: time in milisecond


      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
                
      tags:
        - user's query status

    """

    # print("request-type report: ", requestType, agencyId)
    startTime =request.args.get('startDate')
    endTime = request.args.get('endDate')

    return userQueryStatusReport.getResponse(userId=userId, startTime=startTime, endTime=endTime)








# @reportGenerateBluePrint.route("agency-report/download", methods=['GET'])
# def downloadAgencyReport():

#     # iterate pandas rows to generate table  <table> 'dynamic content from the pandas '</table>  

#     #graphDataProvider.getData(app, request.json)
#     # pdfkit.from_url('http://google.com', 'out.pdf')
    
#     # return agencyReport.getData(current_app)
    
#     print(current_app.root_path)
#     path = os.path.join( current_app.root_path, 'template/driving/')
#     print(path)
#     # path + 'assets/css/bootstrap.min.css', 
#     # css = [path + 'assets/css/driving-license.css']
#     # print(os.path.isfile(css[0] ))
#     print("habijabi")

#     # page = render_template( 'driving-license.html')
#     # pdfkit.from_file(path + 'rakib.html', path +'out.pdf')

#     # pdfkit.from_file(path + '/driving-license.html', path +'out.pdf' , options=options)
#     # pdfkit.from_string(page, path +'out.pdf', css=css)
#     # pdfkit.from_file(path + '/test.html', path +'out.pdf' , options=options)

#     html = render_to_string(path + '/driving-license.html',{'value': "Nowrin"})    
#     pdfkit.from_string(html, path +'out.pdf')
#     # return send_from_directory(directory="static",path ,filename="out.pdf")
#     return send_file(path +'out.pdf', as_attachment=True)
#     # agencyReport.getFile()
