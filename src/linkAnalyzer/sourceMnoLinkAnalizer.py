# import pandas as pd
# import networkx as nx
# from networkx.readwrite import json_graph
# from datetime import datetime
# import json

# from src.constant import constant
# from src.dbService import esService
# from src.services import dateRangeService
# from flask import current_app as app


# def getResponse(body):
#     df = getData(body=body)
#     graphdf = formatData(df, body)
#     graphResponse = createGraph(graphdf)
#     response = makeResponse(graphResponse)
#     return response


# def makeResponse(data):
#     response = {
#         "data": data,
#         "error": None
#     }
#     return response

# def createGraph(df):
#     if(not df.empty):
#         G=nx.from_pandas_edgelist(df, source ='from', target= 'to',  edge_attr = ['duration','numberOfEvents'], create_using=nx.MultiDiGraph())
#         data = json_graph.node_link_data(G)
#         return data
#     else:
#         response = {
#             "directed": True,
#             "graph": {},
#             "links": [],
#             "nodes" : [],
#             "multigraph": True,
#         }

#         return response


# def formatData(df, body):

#     if(not df.empty):
#         df = df[['_source.party_a', '_source.party_b', '_source.usage_type',
#                 '_source.call_duration', '_source.event_time']]
#         df.columns = ['partyA', 'partyB', 'usageType', 'duration', 'eventTime']

#         partyBGroupby = df.groupby(['partyB']).agg({
#             'duration': 'sum',
#             'eventTime': 'count'
#         }).sort_values(['duration', 'eventTime'], ascending=(False, False)).head(body['noOfLinks']).reset_index()['partyB']
#         highestNLinks = df.merge(partyBGroupby, on=['partyB'])
#         app.logger.info('df for highest n links (single source): ', str(highestNLinks))


#         mocdf = highestNLinks[highestNLinks['usageType'] == 'MOC'][['partyA', 'partyB', 'duration', 'eventTime']]
#         mocdf.columns = ['from', 'to', 'duration', 'eventTime']
#         mtcdf = highestNLinks[highestNLinks['usageType'] == 'MTC'][['partyA', 'partyB', 'duration', 'eventTime']]
#         mtcdf.columns = ['to', 'from', 'duration', 'eventTime']
#         concatedDf = pd.concat([mocdf, mtcdf])

#         grpBydf = concatedDf.groupby(['from', 'to']).agg({
#             'duration': 'sum',
#             'eventTime': 'count'
#         })
#         graphdf = grpBydf.reset_index().rename(columns={'eventTime': 'numberOfEvents'})
#         graphdf

#         app.logger.info('df for highest n links incoming outgoing links (single source): ', str(graphdf))
#         return graphdf
    
#     else:
#         return df


# def getData(body):
#     esQuery = buildQuery(body)
#     esData = esService.search('cdr', esQuery)
#     df = pd.json_normalize(esData)
#     return df


# def buildQuery(body):

#     startDate = datetime.fromtimestamp(int(body["startDate"])).strftime("%Y%m%d%H%M%S") if 'startDate'  in body else None
#     endDate = datetime.fromtimestamp(int(body["endDate"])).strftime("%Y%m%d%H%M%S") if 'endDate' in body else None

#     selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]

#     esQuery = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {
#                         "terms": {
#                             selectionCriteria: body['searchValue']
#                         }
#                     },
#                     {
#                         "range": {
#                             "event_time": {
#                                 "gte": startDate,
#                                 "lte": endDate
#                             }
#                         }
#                     }
#                 ],
#                 "must_not": [],
#                 "should": []
#             }
#         },

#         "_source": [
#             "party_a",
#             "party_b",
#             "usage_type",
#             "call_duration",
#             "event_time"
#         ]

#     }

#     return esQuery
