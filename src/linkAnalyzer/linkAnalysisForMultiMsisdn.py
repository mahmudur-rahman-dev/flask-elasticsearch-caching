from flask import current_app as app
import asyncio
import threading
from . import generateLinkAnalysisGraph

from src.dbService import cdrSearch
import pandas as pd


def getResponse(body, generateBy):
    # result  = asyncio.get_event_loop().run_until_complete(getDataAsynchronously(body))
    result = asyncio.run(getDataAsynchronously(body, generateBy))
    return {"data": result, "error": None}


async def getDataAsynchronously(body, generateBy):
    tasks = []
    for element in body:
        task = asyncio.create_task(getAllResponse(element, generateBy))
        tasks.append(task)
    results = await asyncio.gather(*tasks)

    combinedGraph = {
        "directed": True,
        "graph": {},
        "multigraph": True,
        "links": [],
        "nodes": []
    }

    for result in results:
        combinedGraph['links'] = combinedGraph['links']+result['linkAnalysisData']['links']
        combinedGraph['nodes'] = combinedGraph['nodes']+result['linkAnalysisData']['nodes']

    return combinedGraph


async def getAllResponse(body, generateBy):
    # name = threading.currentThread().getName()
    # app.logger.info(f'------------------------------------thread nama {name}--------------------------------------\n')

    # esData = await cdrSearch.getCdrFromEsInTimeRange(body['searchCriteria'], body['searchValue'], body['startDate'], body['endDate'])
    # df = pd.json_normalize(esData)

    response = {
        'searchedWith': body['msisdns']
    }
    
    response['linkAnalysisData'] =  generateLinkAnalysisGraph.getResponse(body, generateBy)['data']
    

    return response
