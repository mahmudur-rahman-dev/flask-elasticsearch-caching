"""Class-based Flask app configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Configuration from environment variables."""

    ENV = environ.get("FLASK_ENV")
    FLASK_APP = "app.py"
    FLASK_HOST = "localhost"


class ProductionConfig(Config):
    # TESTING = True
    FLASK_PORT = 5005
    DEBUG = True
    FROM_CACHE = True
    DB_NAME = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""

    # ES config
    ES_USERNAME = ""
    ES_PASSWORD = ""
    # ES_HOST = "10.101.81.11"
    ES_HOST = "10.101.17.131"
    ES_PORT = "9200"

    REDIS_HOST = "10.101.17.140"
    REDIS_PORT = "6379"
    REDIS_PASSWORD = "a-very-complex-password-here"
    REDIS_DB = 0
    CASE_MANAGEMENT_HOST = 'http://dip-case-management:8585'
    CASE_MANAGEMENT_UNIFIED_VIEWER_CREATION_URL = '/case-management/api/v1/private/cases/unified-viewer/search-summary'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_1 = '/case-management/api/v1/private/cases/discovery/'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_2 = '/unified-viewer/search-summary'
    ENQUERUER_URL = "http://dip-enquerer:6060/enqueuer/api/v1/private/"
    CASE_MANAGEMENT_URL = 'http://dip-case-management:8585/case-management/api/v1/private/cases/fetch-date-range/'

    # should use production config here
    KEYCLOAK_HOST =  "http://dip-keycloak-prod:8080"
    KEYCLOAK_REALM =  "Dip"
    KEYCLOAK_USERNAME = "admin"
    KEYCLOAK_PASSWORD = "Pa55w0rd"



class StagingConfig(Config):
    # TESTING = True
    FLASK_PORT = 5005
    DEBUG = True
    FROM_CACHE = True
    DB_NAME = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""

    # ES config
    ES_USERNAME = ""
    ES_PASSWORD = ""
    # ES_HOST = "10.101.81.11"
    ES_HOST = "10.101.80.5"
    ES_PORT = "9200"

    REDIS_HOST = "10.101.81.11"
    REDIS_PORT = "6379"
    REDIS_PASSWORD = ""
    REDIS_DB = 0
    ENQUERUER_URL = "http://10.101.81.11:6060/enqueuer/api/v1/private/"
    CASE_MANAGEMENT_HOST = 'http://dip-case-management:8585'
    CASE_MANAGEMENT_UNIFIED_VIEWER_CREATION_URL = '/case-management/api/v1/private/cases/unified-viewer/search-summary'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_1 = '/case-management/api/v1/private/cases/discovery/'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_2 = '/unified-viewer/search-summary'
    CASE_MANAGEMENT_URL = 'http://dip-case-management:8585/case-management/api/v1/private/cases/fetch-date-range/'

    KEYCLOAK_HOST = "http://10.101.81.11"
    KEYCLOAK_REALM = "Dip"
    KEYCLOAK_USERNAME = "admin"
    KEYCLOAK_PASSWORD = "759945"

# class DevelopmentConfig(Config):
#     TESTING = True
#     DEBUG = True
#     FLASK_PORT = 5000
#     #posgres config
#     DB_NAME = "dipCaseManagement"
#     DB_USERNAME = "rakib"
#     DB_PASSWORD = "asdqwe123"

#     ES_USERNAME = "elastic"
#     ES_PASSWORD = "Z3bA846YmQdbTHt8Mxq4"
#     ES_HOST = "202.181.14.20"
#     ES_PORT = "1180"

#     REDIS_HOST = "202.181.14.21"
#     REDIS_PORT = "6379"
#     REDIS_PASSWORD = "Ais1#Ais1"
#     REDIS_DB = 0
#     ENQUERUER_URL ="http://202.181.14.19:6060/enqueuer/api/v1/private/"
#     CASE_MANAGEMENT_URL = 'http://202.181.14.19:8585/case-management/api/v1/private/cases/fetch-date-range/'


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    FROM_CACHE = True
    FLASK_PORT = 5000
    # posgres config
    DB_NAME = "dipCaseManagement"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "75994539964468957977"

    ES_USERNAME = "elastic"
    ES_PASSWORD = "janina"
    ES_HOST = "10.101.3.175"
    ES_PORT = "9200"

    REDIS_HOST = "10.101.3.175"
    REDIS_PORT = "6379"
    REDIS_PASSWORD = ""
    REDIS_DB = 0
    
    CASE_MANAGEMENT_HOST= 'http://10.101.3.175:8585'
    ENQUERUER_URL ="http://10.101.3.175:6060/enqueuer/api/v1/private/"
    CASE_MANAGEMENT_URL = 'http://10.101.3.175:8585/case-management/api/v1/private/cases/fetch-date-range/'

    KEYCLOAK_HOST =  "https://202.181.14.26:8443"
    KEYCLOAK_REALM =  "Dip"
    KEYCLOAK_USERNAME = "admin"
    KEYCLOAK_PASSWORD = "75994539964468957977"

    CASE_MANAGEMENT_HOST = 'http://10.101.3.175:8585'
    CASE_MANAGEMENT_UNIFIED_VIEWER_CREATION_URL = '/case-management/api/v1/private/cases/unified-viewer/search-summary'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_1 = '/case-management/api/v1/private/cases/discovery/'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_2 = '/unified-viewer/search-summary'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    FLASK_PORT = 5005

    FROM_CACHE = False

    DB_NAME = "dipCaseManagement"
    DB_USERNAME = "rakib"
    DB_PASSWORD = "asdqwe123"

    # ES_USERNAME = "elastic"
    # ES_PASSWORD = "Z3bA846YmQdbTHt8Mxq4"
    # ES_HOST = "202.181.14.20"
    # ES_PORT = "1180"
    ES_HOST = "202.181.14.26"
    ES_PORT = "9200"
    ES_USERNAME = ""
    ES_PASSWORD = ""

    REDIS_HOST = "localhost"
    REDIS_PORT = "6379"
    REDIS_PASSWORD = ""
    REDIS_DB = 0


    CASE_MANAGEMENT_UNIFIED_VIEWER_CREATION_URL = '/case-management/api/v1/private/cases/unified-viewer/search-summary'
    ENQUERUER_URL ="http://localhost:6060/enqueuer/api/v1/private/"
    CASE_MANAGEMENT_HOST= 'http://10.101.3.175:8585'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_1 ='/case-management/api/v1/private/cases/discovery/'
    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_2 ='/unified-viewer/search-summary'
    CASE_MANAGEMENT_URL = 'http://202.181.14.19:8585/case-management/api/v1/private/cases/fetch-date-range/'

    KEYCLOAK_HOST =  "https://202.181.14.26:8443"
    KEYCLOAK_REALM =  "Dip"
    KEYCLOAK_USERNAME = "admin"
    KEYCLOAK_PASSWORD = "75994539964468957977"


    CASE_MANAGEMENT_UNIFIED_VIEWER_URL_2 = '/unified-viewer/search-summary'
    CASE_MANAGEMENT_URL = 'http://10.101.3.175:8585/case-management/api/v1/private/cases/fetch-date-range/'

    # KEYCLOAK_HOST = "http://10.101.3.175"
    # KEYCLOAK_REALM = "Dip"
