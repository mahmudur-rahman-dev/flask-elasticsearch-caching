from flask import Flask,jsonify
from . import mnoBluePrint
from . import nationalDbBluePrint
from . import mnoScenarioBluePrint
from . import nationalDbScenarioBluePrint
from . import unifiedViewerBluePrint
from . import dataAnalysisBluePrint
from . import appBluePrint
from . import reportGenerateBluePrint
from . import linkAnalysisBluePrint
from . import elasticSearchQueryBluePrint
from . import dashboardUserSummaryBluePrint
from . import targetProfileAnalysisBluePrint

from .api_spec import spec
from .swagger import swagger_ui_blueprint, SWAGGER_URL
from flask_cors import CORS
from src.dbConfig import dbConfig

def createApp():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestingConfig")
    elif app.config["ENV"] == "staging":
        app.config.from_object("config.StagingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    #config redis & es
    try:
        app.redis_client = dbConfig.getRedisConfig(app)
        app.es_client = dbConfig.getEsConfig(app)
    except:
        app.logger.info("ES or Redis Configuration Failed")


    app.register_blueprint(mnoBluePrint.mnoBluePrint)
    app.register_blueprint(nationalDbBluePrint.nationalDbBluePrint)

    app.register_blueprint(mnoScenarioBluePrint.mnoScenarioBluePrint)
    app.register_blueprint(nationalDbScenarioBluePrint.nationalDbScenarioBluePrint)
    
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    app.register_blueprint(unifiedViewerBluePrint.unifiedViewerBluePrint)

    app.register_blueprint(dataAnalysisBluePrint.dataAnalysisBluePrint)
    app.register_blueprint(reportGenerateBluePrint.reportGenerateBluePrint)
    app.register_blueprint(linkAnalysisBluePrint.linkAnalysisBluePrint)
    app.register_blueprint(elasticSearchQueryBluePrint.elasticSearchQueryBluePrint)
    app.register_blueprint(dashboardUserSummaryBluePrint.dashboardUserSummaryBluePrint)
    app.register_blueprint(targetProfileAnalysisBluePrint.targetProfileAnalysisBluePrint)

    
    with app.test_request_context():
    # register all swagger documented functions here
        for fn_name in app.view_functions:
            app.logger.info(fn_name)
            if fn_name == 'static':
                continue
            app.logger.info(f"Loading swagger docs for function: {fn_name}")
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)
            
    app.logger.info(f'ENV is set to: {app.config["ENV"]}')
    
    app.register_blueprint(appBluePrint.appBluePrint)

    CORS(app)
    app.logger.info(f"APP Config: {app.config}")
    # app.logger.info("App Config:"+str(app.config))
    return app