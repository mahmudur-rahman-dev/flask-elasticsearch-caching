from flask import Flask, Blueprint, current_app as app, request, send_from_directory, send_file, render_template

from src.targetProfileInfoProvider import targetProfileProvider

targetProfileAnalysisBluePrint = Blueprint(
    'targetProfileAnalysisBluePrint', __name__, url_prefix="/query-service/api/v1/private/target/analysis")


@targetProfileAnalysisBluePrint.route('profile', methods = ['POST'])
def getTargetProfile():
    return targetProfileProvider.getResponse(request.json)
