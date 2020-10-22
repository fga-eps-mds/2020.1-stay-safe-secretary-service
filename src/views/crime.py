from flask import Blueprint, request
from flask_cors import CORS

from controllers import crime as controller
from utils.formatters import create_response


crime_blueprint = Blueprint('crime', __name__, url_prefix='/api')
CORS(crime_blueprint)


@crime_blueprint.route('/')
def get_crimes():
    if request.method == 'GET':
        response, status = controller.get_all_crimes(params=request.args,
            per_capita=request.headers.get('per_capita'))

    return create_response(response, status)
