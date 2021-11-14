from . import redisSubscribeService
import networkx as nx
from networkx.readwrite import json_graph
import json
import pandas as pd
from src.constant import constant
from src.dbService import esService
from src.services import dateRangeService
from datetime import datetime
from flask import current_app as app
from src.util import msisdnPrefix

generateDFBy = {
    'call-count' : 'eventTime',
    'sms-count' : 'eventTime',
    'total-duration' : 'duration'
}

numberOflinks = 10

def getResponse(body, generateBy):
    body['msisdns'] = [msisdnPrefix.getMobileNoWithDoubleEightAsPrefix(i) for i in body['msisdns']]
    df = getData(body=body)
    app.logger.info(f'data from es (for msisdn linked graph) for request {body}:\n {df}')
    formatedDf = formatData(df, body, generateBy)
    app.logger.info(f'formated df (for msisdn linked graph) for request {body}:\n {formatedDf}')
    graphData = createGraph(formatedDf)
    return makeResponse(data=graphData)


def makeResponse(data):
    response = {
        "data": data,
        "error": None
    }
    return response



def createGraph(df):
    if(not df.empty):
        # app.logger.info(f"df for graph data (multi msisdn): \n{df}")
        G=nx.from_pandas_edgelist(df, source ='from', target= 'to',  edge_attr = ['duration','numberOfEvents'], create_using=nx.MultiDiGraph())
        data = json_graph.node_link_data(G)
        app.logger.info(f"graph data (multi msisdn): \n{data}")
        return data
    else:
        response = {
            "directed": True,
            "graph": {},
            "links": [],
            "nodes" : [],
            "multigraph": True,
        }
        return response


def formatData(df, body, generateBy):

    if(not df.empty):
        df = df[['_source.party_a' , '_source.party_b', '_source.usage_type' ,  '_source.call_duration', '_source.event_time']]
        df.columns = ['partyA', 'partyB','usageType' ,'duration','eventTime']
        df = filterDf(df, generateBy)

        # for highest N links which have most duration
        partyBGroupby = df.groupby(['partyA','partyB']).agg({
            'duration': 'sum',
            'eventTime' : 'count'
        })
        app.logger.info(f'groupby given msisdn: \n{partyBGroupby}')

        numberOflinks = body['noOfLinks'] if 'noOfLinks' in body else 10
        #give highest n links for every msisdn
        mostNLinksForEachAparty = partyBGroupby[generateDFBy[generateBy]].groupby('partyA', group_keys=False).nlargest(numberOflinks).reset_index()[['partyA', 'partyB']]
        highestNLinks = df.merge(mostNLinksForEachAparty,on=['partyA','partyB'])
        app.logger.info(f'df for every {numberOflinks} links: \n{highestNLinks}')

        #creating directinal df for MOC and MTC or SMSMO and SMSMT
        mocdf = highestNLinks[(highestNLinks['usageType']=='MOC')| (highestNLinks['usageType']=='SMSMO')][['partyA', 'partyB' ,'duration','eventTime']]
        mocdf.columns = ['from', 'to' ,'duration', 'eventTime']
        mtcdf = highestNLinks[(highestNLinks['usageType']=='MTC')| (highestNLinks['usageType']=='SMSMT')][['partyA', 'partyB' ,'duration','eventTime']]
        mtcdf.columns = ['to', 'from','duration' ,'eventTime']
        concatedDf = pd.concat([mocdf,mtcdf])
        grpBydf = concatedDf.groupby(['from', 'to']).agg({
            'duration' : 'sum',
            'eventTime' : 'count'
        })
        graphdf = grpBydf.reset_index().rename(columns={'eventTime': 'numberOfEvents'})
            
        return graphdf
    
    else: 
        return df

def filterDf(df, filterBy):
    if(filterBy=='call-count'):
        return df[(df['usageType']=='MOC') | (df['usageType']=='MTC')]
    elif(filterBy=='sms-count'):
        return df[(df['usageType']=='SMSMO') | (df['usageType']=='SMSMT')]
    return df

def getData(body):
    esQuery = buildQuery(body)
    esData = esService.search('cdr', esQuery)
    df = pd.json_normalize(esData)
    app.logger.info("Data from es(for multi msisdn linked graph data): "+ str(df))
    return df


def buildQuery(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime("%Y%m%d%H%M%S") if 'startDate'  in body else None
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime("%Y%m%d%H%M%S") if 'endDate' in body else None

    esQuery = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "party_a": body['msisdns']
                        }
                    },
                    {
                        "range": {
                            "event_time": {
                                "gte": startDate,
                                "lte": endDate
                            }
                        }
                    }
                ],
                "must_not": [],
                "should": []
            }
        },

        "_source": [
            "party_a",
            "party_b",
            "usage_type",
            "call_duration",
            "event_time"
        ]

    }

    app.logger.info(f'query for request-body {body}: {esQuery}')

    return esQuery

