from flask import Flask
from flask_cors import CORS

from views.crime import crime_blueprint

app = Flask(__name__)
app.register_blueprint(crime_blueprint)

CORS(app, automatic_options=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
