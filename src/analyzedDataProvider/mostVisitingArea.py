# import pandas as pd
# from elasticsearch import Elasticsearch
# from src.dbConfig import dbConfig
# from src.constant import constant
# from datetime import datetime


# def getData(app, body):
#     es = dbConfig.getEsConfig(app)
#     esData = searchDataES(es, body)
#     df = pd.json_normalize(esData)
#     print(df)

#     return formatData(df)


# def formatData(df):
#     if (not df.empty):
#         df_location = df.groupby(["_source.lac_start_a", "_source.bts.bts_id",
#                                  '_source.bts.latitude', '_source.bts.longitude'])['_source.event_time'].count()
#         df_location = df_location.reset_index()
#         frequent_area = df_location.sort_values(
#             '_source.event_time', ascending=False).drop_duplicates(['_source.lac_start_a'])
#         frequent_area.columns = ['lac', 'bts', 'latitude', 'longitude', 'event_count']
#         print(frequent_area)
#         return frequent_area.to_dict(orient="records")
        

#     return "No data"


# def searchDataES(es, body):
#     esQuery = buildQuery(body)
#     esData = es.search(index="cdr", body=esQuery)
#     return esData['hits']['hits']


# def buildQuery(body):

#     startDate = datetime.fromtimestamp(
#         int(body["startDate"])).strftime("%Y%m%d%H%M%S")
#     endDate = datetime.fromtimestamp(
#         int(body["endDate"])).strftime("%Y%m%d%H%M%S")
#     selectionCriteria = constant.esCDRSearchCriteriaDict[body['searchCriteria'].upper()]
#     print(selectionCriteria)
#     count = 100

#     if('count' in body):
#         print("count number: ",int(body['count']))
#         count = int(body['count'])

#     esQuery = {
#         "sort": [
#             {
#                 "event_time.keyword": "desc"
#             }
#         ],
#         "query": {
#             "bool": {
#                 "must": [
                    
#                         {
#                             "match": {
#                                 selectionCriteria : body['searchValue']
#                             }
#                         },

#                         {
#                             "range": {
#                                 "event_time": {
#                                     "gte": startDate,
#                                     "lte": endDate
#                                 }
#                             }
#                         }
                    
#                 ],
#                 "must_not": [],
#                 "should": []
#             }
#         },
#         "_source": [
#             "event_time",
#             "lac_start_a",
#             "ci_start_a",
#             "bts"

#         ],
#         "size": count
#     }
#     return esQuery
