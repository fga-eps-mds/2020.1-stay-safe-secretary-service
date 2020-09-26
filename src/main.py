from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from views.crime import crime_blueprint

swagger_blueprint = get_swaggerui_blueprint(
    '/api/docs',
    '/static/swagger.json',
    config={
        'app_name': "Secretary Service - Stay Safe"
    }
)


app = Flask(__name__)
app.register_blueprint(crime_blueprint)
app.register_blueprint(swagger_blueprint, url_prefix='/api/docs')

CORS(app, automatic_options=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
