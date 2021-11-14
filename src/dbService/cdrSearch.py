from flask import current_app as app

from . import esService
from src.constant import constant
import threading

async def getCdrFromEsInTimeRange(searchCriteria, searchValue, startDate, endDate):
    thread_name = threading.current_thread().name
    app.logger.info(f'----------------------------------------------threadddd name: {thread_name}--------------------------------------------------------\n')
    app.logger.info(f'search values {searchCriteria} {searchValue} {startDate} {endDate}')
    selectionCriteria = constant.esCDRSearchCriteriaDict[searchCriteria.upper()]

    esQuery = {
        "sort": [
            {
                selectionCriteria+".keyword": "desc"
            },

            {
                "event_time.keyword": "desc"
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            selectionCriteria: searchValue
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
        }

    }

    esData = esService.search('cdr', esQuery)

    return esData
