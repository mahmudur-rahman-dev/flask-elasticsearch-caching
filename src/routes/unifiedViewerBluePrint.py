from flask import Flask, Blueprint, current_app, request
from src.services import unifiedViewerService


unifiedViewerBluePrint = Blueprint('unifiedViewerBluePrint', __name__,
                         url_prefix="/cases/unified-viewer")


@unifiedViewerBluePrint.route('/<int:id>/generate', methods=['GET'])
async def callUnifiedViewerService(id):
    channel = request.args.get('channel')
    return await unifiedViewerService.getData(id,channel)

