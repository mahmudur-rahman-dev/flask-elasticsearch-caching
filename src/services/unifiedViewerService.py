import asyncio
from src.dbConfig import dbConfig
from flask import current_app as app
import pendulum
from datetime import datetime
import requests
from src.constant.constant import INDEX, UnifiedViewerGroups, getIndexColumns, UnifiedViewerMapper

from src.services.redisPublishService import publishToRedis


async def getDataFromES(index, body, value):
    """
    - Updated by Sadman007

    Retrieves data from Elasticsearch.
    Parameters
        ----------
        index : str 
            index (table) to be searched in Elasticsearch
        body : str
            query body (JSON Object) for Elasticsearch
        value : str
            searched with data
    Returns
        ----------
    data : dict

    """
    try:
        data = None
        esClient = dbConfig.getAsyncElasticsearch(app)
        data = await esClient.search(index=index, body=body)
        data['searchedWith'] = value
        return data
    except Exception as e:
        app.logger.warning("Index not exists in es.")
        app.logger.warning(e)
        app.logger.info("index: " + index + " value: " + value + " body: " + str(body))
        return None


def getSearchCriteria(searchCriteria, value, additionalSearchParams):
    return {'searchCriteria': searchCriteria, 'value': value, 'additionalSearchParams': additionalSearchParams}


def getUnifiedViewerFromPosgres(id):
    """
        The method takes a discoveryId. A post call maked to case managment api which returns a list search information to make a unified viewer
        Parameters
        ----------
        discoveryId : int
            discovery id of the the unified viewer
    """
    url = f"{app.config['CASE_MANAGEMENT_HOST']}{app.config['CASE_MANAGEMENT_UNIFIED_VIEWER_URL_1']}{id}{app.config['CASE_MANAGEMENT_UNIFIED_VIEWER_URL_2']}"
    res = requests.get(url=url).json()
    return res

def getIndexColumnsValues(datas, searchCriterias):
    """
    The method takes a list of search information and a empty list.This method separate out the index,column and value from the search information list. 
    .The separated values are store as list of tuples Eg. [(index,column,value)]. Returns a dict with single base tuple and dataTuples which a set of 
    list of tuples.
        Parameters
        ----------
        discoveryId : int
            discovery id of the the unified viewer
        searchCriterias : list of dict
            list of dict where dict contain searchCriteria and search value of unified viewer base
    """
    app.logger.info("Search summary for unified viewer: ")
    app.logger.info(datas)
    indexs = []
    columns = []
    values = []
    baseData = min(datas, key=lambda x: x['id'])
    datas.remove(baseData)
    newData = [baseData]
    newData.extend(datas)
    seen = set()
    for data in newData:
        index = INDEX[data['dipRequestTypeId']]
        searchCriteriaId = data['dipSearchCriteriaId']
        indexs.append(index)
        columns.append(getIndexColumns(data)[index][searchCriteriaId])
        values.append(data['searchValue'])
        if data['unifiedViewerBase']:
            searchCriteria = getSearchCriteria(searchCriteriaId,data['searchValue'], data['additionalSearchParams'])
            if str(searchCriteria) not in seen:
                searchCriterias.append(searchCriteria)
                seen.add(str(searchCriteria))
                
    app.logger.info(indexs)
    app.logger.info(columns)
    app.logger.info(values)
                
    baseTuple = ()
    dataTuples = list()
    if len(indexs) > 0:
        baseTuple = (indexs[0], columns[0], values[0])
        app.logger.info("inside if condition base tuple")
        app.logger.info(baseTuple)
        dataTuples =  set(zip(indexs[1:], columns[1:], values[1:]))
        app.logger.info("inside if condition data tuple")
        app.logger.info(dataTuples)
    
    app.logger.info("outside if condition data tuple")
    app.logger.info(dataTuples)
    result = {'baseTuple': baseTuple, 'dataTuples':dataTuples}
    return result

def addUnifiedViewerGroupsArray(unifiedViewResponse):
    """
    Create empty unified view response dict

    Returns
    ----------
    unifiedViewResponse : dict

    """
    
    unifiedViewResponse['name'] = []
    unifiedViewResponse['photo'] = []
    unifiedViewResponse['mobileNumber'] = []
    unifiedViewResponse['nid10Digit'] = []
    unifiedViewResponse['nid13Digit'] = []
    unifiedViewResponse['nid17Digit'] = []
    unifiedViewResponse['dob'] = []
    unifiedViewResponse['brnNumber'] = []
    unifiedViewResponse['drivingLicenseNumber'] = []
    unifiedViewResponse['passportNumber'] = []
    unifiedViewResponse['perviousPassportNumber'] = []
    unifiedViewResponse['presentAddress'] = []
    unifiedViewResponse['permanentAddress'] = []
    unifiedViewResponse['occupation'] = []
    unifiedViewResponse['gender'] = []
    unifiedViewResponse['spouseName'] = []
    unifiedViewResponse['fatherName'] = []
    unifiedViewResponse['motherName'] = []

def generateSerializedPresentAddress(presentAddress):
    app.logger.info("Processing present address")
    app.logger.info(presentAddress)
    
    if not presentAddress:
        return None
    serializedAddress = (presentAddress['home_or_holding_no'] + ' ') if ('home_or_holding_no' in presentAddress and presentAddress['home_or_holding_no'] is not None) else ''
    serializedAddress += (presentAddress['mouza_or_moholla'] + ' ') if ('mouza_or_moholla' in presentAddress and presentAddress['mouza_or_moholla'] is not None) else ''
    serializedAddress += (presentAddress['additional_mouza_or_moholla'] + ' ') if ('additional_mouza_or_moholla' in presentAddress and presentAddress['additional_mouza_or_moholla'] is not None) else ''
    serializedAddress += (presentAddress['village_or_road'] + ' ') if ('village_or_road' in presentAddress and presentAddress['village_or_road'] is not None) else ''
    serializedAddress += (presentAddress['additional_village_or_road'] + ' ') if ('additional_village_or_road' in presentAddress and presentAddress['additional_village_or_road'] is not None) else ''
    serializedAddress += (presentAddress['union_or_ward'] + ' ') if ('union_or_ward' in presentAddress and presentAddress['union_or_ward'] is not None) else ''
    serializedAddress += (presentAddress['upozilla'] + ' ') if ('upozilla' in presentAddress and presentAddress['upozilla'] is not None) else ''
    serializedAddress += (presentAddress['city_corporation_or_municipality'] + ' ') if ('city_corporation_or_municipality' in presentAddress and presentAddress['city_corporation_or_municipality'] is not None) else ''
    app.logger.info("returning present address")
    app.logger.info(serializedAddress)
    return serializedAddress

def generateSerializedPermanentAddress(permanentAddress):
    app.logger.info("Processing permanent address")
    app.logger.info(permanentAddress)

    if not permanentAddress:
        return None
    serializedAddress = (permanentAddress['home_or_holding_no'] + ' ') if ('home_or_holding_no' in permanentAddress and permanentAddress['home_or_holding_no'] is not None) else ''
    serializedAddress += (permanentAddress['mouza_or_moholla'] + ' ') if ('mouza_or_moholla' in permanentAddress and permanentAddress['mouza_or_moholla'] is not None) else ''
    serializedAddress += (permanentAddress['additional_mouza_or_moholla'] + ' ') if ('additional_mouza_or_moholla' in permanentAddress and permanentAddress['additional_mouza_or_moholla'] is not None) else ''
    serializedAddress += (permanentAddress['additional_village_or_road'] + ' ') if ('additional_village_or_road' in permanentAddress and permanentAddress['additional_village_or_road'] is not None) else ''
    serializedAddress += (permanentAddress['union_or_ward'] + ' ') if ('union_or_ward' in permanentAddress and permanentAddress['union_or_ward'] is not None) else ''
    serializedAddress += (permanentAddress['upozilla'] + ' ') if ('upozilla' in permanentAddress and permanentAddress['upozilla'] is not None) else ''
    serializedAddress += (permanentAddress['rmo'] + ' ') if ('rmo' in permanentAddress and permanentAddress['rmo'] is not None) else ''
    app.logger.info("returning permanent address")
    app.logger.info(serializedAddress)
    return serializedAddress

def getValue(groupName, value):
    checkValue = f"nid{len(str(value))}Digit"
    if groupName == checkValue:
        return value
    elif groupName == 'nid10Digit' or groupName == 'nid13Digit' or groupName == 'nid17Digit':
        return ''
    else:
        return value


def getCompareStatus(compareValue, baseValue):
    """
    Compare the two values and return True/False
    Returns
    ----------
    boolean : True/False

    """
    if compareValue == baseValue:
        return True
    return False


def getSingleObj(result, groupName, searchedWith, unifiedViewResponse):
    """
        This method process the result from elastic search to make the group object.
        Parameters
        ----------
        result : dict 
            data received from elasticsearch
        groupName:str
            name of the group for which this object will be made
        searchedWith: str
            search value for which result was found
        unifiedViewResponse:dict
            this dict contain base unified viewer to make comparison.
        Returns
        ----------
        singleObject : dict 
    """


    app.logger.info("will start data processing for the following group")
    app.logger.info(groupName)

    obj = dict()
    obj['type'] = result['_index']
    app.logger.info("Object type: ")
    app.logger.info(obj['type'])

    columnName = UnifiedViewerMapper[obj['type']][groupName]
    app.logger.info("column name")
    app.logger.info(columnName)

    obj['value'] = getValue(groupName, result['_source']
                            [columnName]) if columnName in result['_source'] else None
    if groupName == 'presentAddress' and obj['type'] == 'nid':
        obj['value'] = generateSerializedPresentAddress(obj['value'])
    elif groupName == 'permanentAddress' and obj['type'] == 'nid':
        obj['value'] = generateSerializedPermanentAddress(obj['value'])
    app.logger.info("Object value: ")
    app.logger.info(obj['value'])

    idColumn = UnifiedViewerMapper[obj['type']]['id']
    app.logger.info("Object id: ")
    app.logger.info(idColumn)

    if obj['type'] == 'nid' and (groupName == 'nid10Digit' or groupName == 'nid13Digit' or groupName == 'nid17Digit'):
        obj['type'] = groupName
        obj['id'] = obj['value']
    elif obj['type'] == 'nid':
        obj['id'] = result['_source'][idColumn] if idColumn in result['_source'] else None
        obj['type'] = f"nid{len(str(obj['id']))}Digit"
    else:
        obj['id'] = result['_source'][idColumn] if idColumn in result['_source'] else None
    obj['searchedWith'] = searchedWith
    if groupName == 'dob':
        if type(obj['value']) is int:
            obj['value'] = pendulum.from_timestamp(
                obj['value']/1000).format('YYYY-MM-DD')
        else:
            obj['value'] = pendulum.parse(obj['value']).format('YYYY-MM-DD')
    if len(unifiedViewResponse[groupName]) > 0:
        obj['compareStatus'] = getCompareStatus(
            obj['value'], unifiedViewResponse[groupName][0]['value'])
    else:
        obj['compareStatus'] = True
    app.logger.info("================= end =========================") 
    app.logger.info("================= end =========================")
    return obj


def addDataToGroup(data, groupName, unifiedViewResponse):
    """
    The method is async which call elastic search for data, after recieveing data it is processed and append to unifiedViewResponse group
        Parameters
        ----------
        data : dict
            elastic search query data which will be processed.
        groupName : str 
            group name for which the data will be processed
        unifiedViewResponse : dict
        Returns
        ----------
        groupArray : list of dict of single object
    """


    app.logger.info("fetching data from es with the following group name")
    app.logger.info(groupName)

    esResults = data['hits']['hits']
    groupArray = []
    for result in esResults:
        singleObjecPrams = {'result': result, 'groupName': groupName,
                            'searchedWith': data['searchedWith'], 'unifiedViewResponse': unifiedViewResponse}
        groupArray.append(getSingleObj(**singleObjecPrams))

    return groupArray


def esQueryBody(column, value):
    """
        Returns
        ----------
        esQueryBody : dict 
    """
    return {"query": {
            "bool": {"must": [{"match": {column: value}}], "must_not": [], "should": []}}}


async def getDataFromESAndMakeGroups(esObject, unifiedViewResponse):
    """
    The method is async which call elastic search for data, after recieveing data it is processed and append to unifiedViewResponse group
        Parameters
        ----------
        esObject : dict
            parameter required for elastic search query
        unifiedViewResponse : dict
    """
    esData = await getDataFromES(**esObject)
    if esData is None:
        return
    for groupName in unifiedViewResponse.keys():
        app.logger.info("making group with the following group name")
        app.logger.info(groupName)
        unifiedViewResponse[groupName].extend(addDataToGroup(esData, groupName, unifiedViewResponse))


async def UnifiedViewerMaker(queryData):
    """
    The method takes a list of tuples containing index,column and value. Which are used to retieve data from elasticsearch.
    Returns list of unified viewer groups. Unified viewer groups contain list singleObjecPrams()
        Parameters
        ----------
        queryData : list of tuple
            tuple contains (index,column,value)
        Returns
        ----------
        unifiedViewResponse : dict of list of unified viewer groups
    """
    
    unifiedViewResponse = dict()
    addUnifiedViewerGroupsArray(unifiedViewResponse)
    unifiedViewerCoroutinArray = list()

    (index, column, value) = queryData['baseTuple']
    body = esQueryBody(column, value)
    esObject = {'index': index, 'body': body, 'value': value}
    app.logger.info("Fetching data and making groups with the following index:")
    app.logger.info(esObject)

    await getDataFromESAndMakeGroups(esObject, unifiedViewResponse)

    app.logger.info("data tuples will be looped through now to build unified group")
    app.logger.info(queryData)

    for (index, column, value) in queryData['dataTuples']:
        body = esQueryBody(column, value)
        esObject = {'index': index, 'body': body, 'value': value}
        app.logger.info("Fetching data and making groups with the following index for non base:")
        app.logger.info(esObject)
        data = getDataFromESAndMakeGroups(esObject, unifiedViewResponse)
        unifiedViewerCoroutinArray.append(data)
    await asyncio.gather(*unifiedViewerCoroutinArray)

    return unifiedViewResponse


async def getData(discoveryId, channels):
    """
    The method takes a discoveryId and a channels.Returns completed unifiedViewResponse
        Parameters
        ----------
        discoveryId : int
            discovery id of the the unified viewer
        channel : list of str
            list of channels where the response is publish
    """
    error = None
    unifiedView = None
    searchCriterias = list()
    try:
        unifiedData = getUnifiedViewerFromPosgres(discoveryId)
        queryData = getIndexColumnsValues(unifiedData,searchCriterias)
        app.logger.info("data tuples have been fetched")
        app.logger.info(queryData)
        unifiedView = await UnifiedViewerMaker(queryData)
    except Exception as e:
        app.logger.exception(e)
        error = {
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "status": "INTERNAL_SERVER_ERROR",
            "error": str(e),
            "message": "Could not Generate Unified Viewer"
        }
    response = {
        'data': {'searchCriterias': searchCriterias, 'unifiedView': unifiedView , 'unifiedGroup': UnifiedViewerGroups},
        'error': error,
        'type': "UNIFIED_VIEW",
        'unifiedViewerId': unifiedData[0]['unifiedViewerId'] if 'unifiedViewerId' in unifiedData[0] else None,
    }
    # body = {'searchValue': id, 'channels': [channel]}
    # publishToRedis(body, response)
    return response
