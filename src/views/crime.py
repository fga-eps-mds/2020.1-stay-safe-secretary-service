from flask import Blueprint, request
from flask_cors import CORS

from controllers import crime as controller
from utils.formatters import create_response
from utils.validators.general import validate_header


crime_blueprint = Blueprint('crime', __name__, url_prefix='/api')
CORS(crime_blueprint)


@crime_blueprint.route('/')
@validate_header
def get_crimes():
    secretary = request.args.get('secretary')
    crime = request.args.get('crime')
    city = request.args.get('city')
    initial_month = request.args.get('initial_month')
    final_month = request.args.get('final_month')

    if request.method == 'GET':
        response, status = controller.get_all_crimes(secretary, crime, city,
            initial_month, final_month)

    return create_response(response, status)
