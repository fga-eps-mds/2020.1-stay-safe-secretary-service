from flask import Blueprint, request, render_template, redirect, url_for
from flask_cors import CORS

from database.db import db

index_blueprint = Blueprint('index', __name__, url_prefix='/api')
CORS(index_blueprint)


@index_blueprint.route('/')
def todo():
    _items = db['staysafe'].find()
    items = [item for item in _items]

    return render_template('index.html', items=items)


@index_blueprint.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db['staysafe'].insert_one(item_doc)

    return redirect(url_for('index.todo'))
