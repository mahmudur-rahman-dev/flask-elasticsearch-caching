from .api_spec import spec
from flask import Blueprint,jsonify
from flask import current_app as app
import gitinfo

appBluePrint = Blueprint('appBluePrint', __name__)
@appBluePrint.route("/api/swagger.json")
def create_swagger_spec():
    return jsonify(spec.to_dict())
@appBluePrint.route("/info")
def health():
    info = gitinfo.get_git_info()
    app.logger.info(info)
    return info