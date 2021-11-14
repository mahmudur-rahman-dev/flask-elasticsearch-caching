from elasticsearch import exceptions
from flask import current_app
from src.dbConfig import dbConfig

def search(index,body):

    current_app.logger.info(f'query for es {body}')
    es = current_app.es_client
    # es = dbConfig.getEsConfig(current_app)
    try:
        esData = es.search(index=index, body=body, size=10000, scroll ='2s')['hits']['hits']
        # esData = es.search(index=index, body=body, scroll ='10s',  size=10000, track_total_hits= True)
        # sid = esData['_scroll_id']
        # rs = es.scroll(scroll_id=sid, scroll='10s')
        # current_app.logger.info(f'scrolled data from es: {rs}')
        # eshits = rs['hits']['hits']
    
    except exceptions.NotFoundError:
        esData = []
        print("Elastic Search Fail, NotFoundError")
    current_app.logger.info(f'{esData}')
    return esData

def insert(index_name, docs):
    
    es = current_app.es_client
    es.index(index=index_name,  body=docs)