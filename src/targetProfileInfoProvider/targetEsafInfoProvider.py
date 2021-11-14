from src.dbService import esService


def getResponse(body):
    esData = getData(body=body)
    return makeResponse(esData)


def makeResponse(data):
    if(data):
        return {
            'msisdn' : data['_source']['phone'],
            'name' : data['_source']['name'],
            'nid' : data['_source']['nid'],
            'dob' :  data['_source']['birth_date'],
            'address' : data['_source']['address']
        }
    else:
        return None
     


def getData(body):
    query = buildQuery(body)
    esData = esService.search(index="esaf", body=query)
    if(len(esData)):
       return esData[0] 
    return ''


def buildQuery(body):

    query = {
        "query":
        {
            "bool":
            {
                "must":
                [
                    {
                        "match":
                        {
                            "phone": body["searchValue"]
                        }
                    }
                ]
            }
        }
    }

    return query


