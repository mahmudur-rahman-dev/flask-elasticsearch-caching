from flask import current_app as app
import asyncio
import threading
from . import initiateCdr

from src.dbService import cdrSearch
import pandas as pd


def getResponse(body):   
    result = asyncio.run(getDataAsynchronously(body))
    return {"data": result, "error": None}


async def getDataAsynchronously(body):
    tasks = []
    for element in body:
        task = asyncio.create_task(getAllResponse(element))
        tasks.append(task)
    results = await asyncio.gather(*tasks)

    return results


async def getAllResponse(body):
    return initiateCdr.callBackendForCdr(body)

