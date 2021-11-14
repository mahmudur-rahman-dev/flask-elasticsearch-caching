from src.dbService import esService
from flask import current_app as app
import pandas as  pd
from src.util import agencyIdRetriver

def getResponse(requestType, startTime, endTime):
    df = getData(requestType, startTime, endTime)
    app.logger.info(f'df from es data for request {requestType}\n{df}')
    formatedDf = formatData(df)
    app.logger.info(f'formated df for request {requestType}\n{df}')
    return makeResponse(formatedDf)

def makeResponse(groupbyDf):

    responseRecords = {
        "records" : [],
        "numberOfRecords" : 0
    }
    if(len(groupbyDf) is not 0):
        for agency in groupbyDf.groups:   
            responseRecords["records"].append(makeGroupResponse(groupbyDf, agency))

    responseRecords['numberOfRecords'] = len(responseRecords['records'])
    return {"data": responseRecords, "error": None}

def makeGroupResponse(groupbyDf, agency):
    df = groupbyDf.get_group(agency)

    agencyReport = {
        "agency" : agency,
        "totalQuery" : len(df),
        "totalSuccessfullQuery" : len(df[df['queryStatus'] == 'SUCCESS']) ,
        "totalFailedQuery":len(df[df['queryStatus'] == 'FAILURE'])
    }
    return agencyReport



def formatData(df):
    if not df.empty:
        #ordering requestTypes as success and failure to keep only success requests from same request_uuid        
        app.logger.info(f'df before setting status as category and sorting :\n{df}')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].astype('category')
        df['_source.data_retrieval_status']=df['_source.data_retrieval_status'].cat.set_categories(['SUCCESS', 'FAILURE'], ordered=True)
        app.logger.info(f'df after setting status as category and sorting :\n{df}')
        df.sort_values(['_source.search_summary_uuid', '_source.data_retrieval_status'], inplace=True)
        df.drop_duplicates(subset="_source.search_summary_uuid", inplace=True)
        
        df = df[['_source.agency_id', '_source.data_retrieval_status' ]]
        df.columns = ['agency', 'queryStatus']
        df['agency'] = df['agency'].apply(lambda agencyId: agencyIdRetriver.getAgencyId(agencyId))

        grpByDf = df.groupby('agency')    
        app.logger.info(f'group by df: \n {grpByDf}')
        return grpByDf
    return df

def getData(requestType, startTime, endTime):
    esQuery =  buildQuery(requestType, startTime, endTime)
    esData = esService.search(index='search-summary-log', body=esQuery)
    df = pd.json_normalize(esData)
    return df

def buildQuery(requestType, startTime, endTime):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "request_type": requestType
                        }
                    },
                    {
                        "range": {
                            "searched_at": {
                                "gte": startTime,
                                "lte": endTime
                            }
                        }
                    }
                ],
                "must_not": [],
                "should": []
            }
        },
        "_source" : [
            "agency_id", "data_retrieval_status", "search_summary_uuid"
        ]

    }

    app.logger.info(f'query for es: {query}')


    return query
