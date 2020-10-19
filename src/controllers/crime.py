from database.db import db
from utils.valid_crimes import valid_crimes_df, valid_crimes_sp

def get_all_crimes(secretary, crime, city):
    # validate the params
    if secretary and secretary not in ['sp', 'df']:
        return "Parâmetro secretary inválido", 400

    if crime and crime not in valid_crimes_df and crime not in valid_crimes_sp:
        return "Parâmetro crime inválido", 400

    data = []
    if (secretary == "df" or secretary is None) and (crime in valid_crimes_df or crime is None):
        _data = db['crimes_df'].find(
            { 'cities.name': city } if city else {},
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [valid_crimes_df.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True,
            }
        )
        data += list(_data)
    if (secretary == "sp" or secretary is None) and (crime in valid_crimes_sp or crime is None):
        _data = db['crimes_sp'].find(
            { 'cities.name': city } if city else {},
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [valid_crimes_sp.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True
            }
        )
        data += list(_data)

    return data, 200
