from datetime import datetime


def generaterGraphData(es,body):
   
    esData = esSearch(es,body)

    esCDRHistory = {}

    for data in esData:
        print(data)
        esCDRHistory[data['key']] = data['then_by_usage_type']['buckets']
    
    print(esCDRHistory) 

    return esCDRHistory




def esSearch(es,body):
    
    esQuery = makeCDRQueryString(body)
    esData = es.search(index="cdr", body=esQuery)
    return esData['aggregations']['first_by_partyb']['buckets']

def makeCDRQueryString(body):

    startDate = datetime.fromtimestamp(int(body["startDate"])).strftime("%Y%m%d%H%M%S")
    endDate = datetime.fromtimestamp(int(body["endDate"])).strftime("%Y%m%d%H%M%S")

    esQuery = {
        "query": {
            "bool": {
            "must": [
                {
                "match": {
                    "party_a": body['msisdn']
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
        "aggs": {
            "first_by_partyb": {
            "terms": {
                "field": "party_b.keyword"
            },
            "aggs": {
                "then_by_usage_type": {
                "terms": {
                    "field": "usage_type.keyword"
                }
                }
            }
            }
        }
    }

    return esQuery