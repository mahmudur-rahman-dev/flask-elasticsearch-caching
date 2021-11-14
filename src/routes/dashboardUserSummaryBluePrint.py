from flask import Flask, Blueprint, current_app, request
from src.dashboardUserSummaryGenerator import userInfoProvider
from src.dashboardUserSummaryGenerator import queryBasedActivity
from src.dashboardUserSummaryGenerator import userQueryStateProvider
from src.dashboardUserSummaryGenerator import timeBasedUserActivityProvider

dashboardUserSummaryBluePrint = Blueprint('dashboardUserSummaryBluePrint', __name__,
                         url_prefix="/query-service/api/v1/private/dashboard")

@dashboardUserSummaryBluePrint.route('/user/<string:userId>', methods=['GET'])
def getUserInfo(userId):
    """
    ---
    get:
      summary: Returns a user's information
      parameters:
        - in: path
          name: userId
          schema:
            type: string

      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#'
      tags:
        - user information from keycloak

    """
    return userInfoProvider.getResponse(userId=userId)


@dashboardUserSummaryBluePrint.route('/user/<string:userId>/activity/query-based', methods=['GET'])
def getUserRequestTypeCountGraphData(userId):

    """
    ---
    get:
      summary: Returns a user query-based activity.
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
        - Single user query-based activity

    """

    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    return queryBasedActivity.getResponse(userId=userId, startDate=startDate, endDate= endDate)


@dashboardUserSummaryBluePrint.route('/user/<string:userId>/query-state', methods=['GET'])
def getUserQueryStatus(userId):

    """
    ---
    get:
      summary: Returns a user query state.
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
        - Single user query state

    """

    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    return userQueryStateProvider.getResponse(userId=userId, startDate=startDate, endDate= endDate)


@dashboardUserSummaryBluePrint.route('/user/<string:userId>/activity/time-based', methods=['GET'])
def getTimeBasedUserActivity(userId):

    """
    ---
    get:
      summary: Returns a user's time-based activity.
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
        - Single user time based activity

    """

    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    return timeBasedUserActivityProvider.getResponse(userId=userId, startDate=startDate, endDate= endDate)

