
from flask import Blueprint, request
from flask_cors import CORS

from controllers import coordinates as controller
from utils.formatters import create_response


coordinates_blueprint = Blueprint('coordinates', __name__, url_prefix='/api')
CORS(coordinates_blueprint)


@coordinates_blueprint.route('/coordinates')
def get_coordinates():
    state = request.args.get('state')

    if request.method == 'GET':
        response, status = controller.get_all_coordinates(state)

    return create_response(response, status)