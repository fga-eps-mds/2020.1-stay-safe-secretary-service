from flask import Blueprint, request
from flask_cors import CORS

from controllers import crime as controller
from utils.formatters import create_response
from utils.validators.general import validate_header

from settings import logger

crime_blueprint = Blueprint('crime', __name__, url_prefix='/api')
CORS(crime_blueprint)

@crime_blueprint.route('/')
def get_crimes():
    secretary = request.args.get('secretary')
    crime = request.args.get('crime')

    if request.method == 'GET':
        response, status = controller.get_all_crimes(secretary, crime)

    return create_response(response, status)

