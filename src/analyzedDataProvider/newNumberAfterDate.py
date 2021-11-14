# import pandas as pd
# import json
# from datetime import datetime
# from src.dbConfig import dbConfig
# from src.constant import constant
# from . import multiPhnOnImei

# def getData(app, body):
#     es = dbConfig.getEsConfig(app)
#     # esData = searchDataES(es, body)
#     # df = pd.json_normalize(esData)
#     # esData = multiPhnOnImei.getData(app, body)
#     # df = pd.json_normalize(json.loads)
#     #print(df)

#     # return dataFormation(df)
#     return multiPhnOnImei.getData(app, body)

# def dataFormation(df):

#     if (not df.empty):
#         print(df)
#         df = df[['_source.party_a','_source.event_time']]
#         #df = df.groupby(['_source.party_a','_source.event_time'])['_source.event_time'].size()
#         return df.to_dict(orient="records")

#     return "No data found"

# def searchDataES(es, body):
#     esQuery = buildQuery(body)
#     esData = es.search(index="cdr", body=esQuery)
#     return esData['hits']['hits']


# def buildQuery(body):

#     dateString = datetime.fromtimestamp(int(body["startDate"])).strftime("%Y%m%d%H%M%S")

#     selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]

    
#     esQuery = {
#         "sort": [
#             {
#                 "event_time.keyword": "desc"
#             }
#         ],
#         "query": {
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             selectionCriteria: body['searchValue']
#                         }
#                     },
#                     {
#                         "range": {
#                             "event_time": {
#                                 "gte": dateString
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
#             "event_time"
#         ]
#     }

#     return esQuery
