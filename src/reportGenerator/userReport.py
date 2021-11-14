from flask import Flask, jsonify
import pandas as pd
from datetime import datetime
from src.dbService import esService
import json
from flask import current_app as app
from src.constant import constant
from src.util import agencyIdRetriver
from . import generateKeycloakAccessToken
from . import userInfoKeyCloak


def getResponse(agencyId, startDate, endDate):
    df = getData(agencyId=agencyId, startDate=startDate, endDate=endDate)
    app.logger.info(
        f'for agency: {agencyId}, start-date: {startDate}, end-date: {endDate}, df from es data: \n{df} ')
    formatedDf = formatData(df)
    app.logger.info(
        f'for agency: {agencyId}, start-date: {startDate}, end-date: {endDate}, formated df: \n{formatedDf} ')
    dfWithUser = getDfwithUserInfo(formatedDf)
    app.logger.info(
        f'for agency: {agencyId}, start-date: {startDate}, end-date: {endDate}, df with user info: \n{dfWithUser} ')

    return makeResponse(dfWithUser, agencyId)


def makeResponse(df, agencyId):

    userReportdict = {
        'data': {
            'agency': agencyId if agencyId else 'ALL',
            'records': [],
            'numberOfRecords': 0
        },
        'error': None
    }

    if(not df.empty):
        userReportdict['data']['records'] = df.to_dict(orient='records')
        userReportdict['data']['numberOfRecords'] = len(
            userReportdict['data']['records'])

    return userReportdict


def getDfwithUserInfo(df):
    if(not df.empty):
        accessToken = generateKeycloakAccessToken.getAccessToken()
        df['user'] = df.apply(lambda row: getUserInfofromkeycloak(
            str(row.name), accessToken), axis=1)
        app.logger.info(f'dataframe with user {df}')

    return df


def getUserInfofromkeycloak(userId, accessToken):
    app.logger.info(
        f'access-token to get user info from key-cloak: {accessToken}')
    userInfo = userInfoKeyCloak.getUserInfo(
        userId=userId, accessToken=accessToken)

    user = {
        'id': userId,
        'name': '',
        'userName': ''
    }

    if 'error' not in userInfo:
        app.logger.info('user :' + userId + 'user info: {0}'.format(userInfo))
        user['name'] = f"{userInfo['firstName']} " if(
            'firstName' in userInfo) else ''
        user['name'] = f"{user['name']}{userInfo['lastName']}" if(
            'lastName' in userInfo) else ''
        user['userName'] = userInfo['username'] if(
            'userName' in userInfo) else ''

    app.logger.info(f'user-ID: {userId} , user-info: {userInfo}')

    return user


def getData(agencyId, startDate, endDate):
    esQuery = buildQuery(
        agencyId=agencyId, startDate=startDate, endDate=endDate)
    esData = esService.search(index='search-summary-log', body=esQuery)
    df = pd.json_normalize(esData)
    app.logger.info("Dataframe of search summary data: \n"+str(df))
    return df


def formatData(df):

    if (not df.empty):
        df = df[['_source.agency_id', '_source.user_id', '_source.request_type', '_source.search_summary_uuid']]
        df.columns = ['agency', 'userId', 'request_type', 'search_summary_uuid']
        df.drop_duplicates(subset="search_summary_uuid", inplace=True)
        df['agency'] = df['agency'].apply(lambda agencyId: agencyIdRetriver.getAgencyId(agencyId))

        userWiseReport = df[['userId', 'request_type']].pivot_table(
            index='userId', columns='request_type', aggfunc=len, fill_value=0)
        app.logger.info(f'pivot table after process: \n{userWiseReport}')
        userWiseReport = userWiseReport.reindex(userWiseReport.columns.union(
            constant.TaskTypes, sort=False), axis=1, fill_value=0)
        userWiseReport['TOTAL'] = userWiseReport.sum(axis=1)
        app.logger.info(f'Agency wise summary report table: {userWiseReport}')

        return userWiseReport

    return df


def buildQuery(agencyId, startDate, endDate):
    query = {
        "query": {
            "bool": {
                "must": [

                    {
                        "range": {
                            "searched_at": {
                                "gte": startDate,
                                "lte": endDate
                            }
                        }
                    }
                ]
            }
        },
        "_source": [
            'agency_id', 'user_id', 'request_type', 'search_summary_uuid'
        ]

    }
    if agencyId:
        query["query"]["bool"]["must"].append({
            "wildcard": {
                "agency_id.keyword": "/"+agencyId+"*"
            }
        })
        # query["query"]["regexp"]={
        #     "agency_id": "*"+agencyId+"*"
        # }

    app.logger.info(
        f'query built for es: {agencyId}, {startDate}, {endDate} :\n{query}')
    return query
