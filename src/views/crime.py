from flask import Blueprint, request
from flask_cors import CORS

from controllers import crimes_df as controller_df
from controllers import crimes_sp as controller_sp
from utils.formatters import create_response


crime_blueprint = Blueprint('crime', __name__, url_prefix='/api')
CORS(crime_blueprint)


@crime_blueprint.route('/')
def get_crimes():
    secretary = request.args.get('secretary')

    if request.method == 'GET':
        if secretary == 'df':
            response, status = controller_df.get_all_crimes_df(params=request.args,
                per_capita=request.headers.get('per_capita'))
        elif secretary == 'sp':
            response, status = controller_sp.get_all_crimes_sp(params=request.args,
                per_capita=request.headers.get('per_capita'))
        else:
            response, status = (
                'Parâmetro secretary inválido ou inexistente.', 400)

    return create_response(response, status)
