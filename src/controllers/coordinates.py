from database.db import db


def get_all_coordinates(state):
    # validate the params
    if state not in ['sp']:
        return "Parâmetro state inválido", 400

    # getting the data
    data = []
    if state == "sp":
        _data = db['coordinates'].find({}, {'_id': False})
        data += list(_data)

    return data, 200
