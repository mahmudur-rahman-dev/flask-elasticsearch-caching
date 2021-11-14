from elasticsearch import Elasticsearch ,AsyncElasticsearch

import redis
def getEsConfig(app):
    #  Elasticsearch(['http://'+app.config[""]+':'+app.config[""]+'@'+202.181.14.19:9200'])
    # Elasticsearch.index()
    if len(app.config["ES_USERNAME"])==0:
        return Elasticsearch(hosts=app.config["ES_HOST"],port= app.config["ES_PORT"])
    return Elasticsearch(hosts=app.config["ES_HOST"],port= app.config["ES_PORT"],http_auth=(app.config["ES_USERNAME"], app.config["ES_PASSWORD"]))
def getRedisConfig(app):
    if len(app.config["REDIS_PASSWORD"]) == 0:
        # return redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0)
        return redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=0, charset="utf-8", decode_responses=True)
    else:
        # return redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], password=app.config["REDIS_PASSWORD"], db=0)
        return redis.StrictRedis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], password=app.config["REDIS_PASSWORD"], db=0, charset="utf-8", decode_responses=True)

def getAsyncElasticsearch(app):
    if len(app.config["ES_USERNAME"])==0:
        return AsyncElasticsearch(hosts=app.config["ES_HOST"],port= app.config["ES_PORT"])
    return AsyncElasticsearch(hosts=app.config["ES_HOST"],port= app.config["ES_PORT"],http_auth=(app.config["ES_USERNAME"], app.config["ES_PASSWORD"]))

def getPostgresConfig ():
    # con = psycopg2.connect(database=app.config["DB_NAME"], user=app.config["DB_USERNAME"], password=app.config["DB_PASSWORD"], host="localhost", port="5432")
    # cursor = con.cursor()
    # cursor.execute("select * from dip_case_management.dip_search_criteria")
    # result = cursor.fetchall()
    pass

# def getKeyCloakConfig (app):
#     app.config["KEYCLOAK_HOST"]