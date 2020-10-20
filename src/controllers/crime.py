from database.db import db
from utils.filters.valid_crimes import valid_crimes_df, valid_crimes_sp
from utils.filters.valid_months import get_all_valid_months
from utils.filters.crimes_filters import get_cumulative_amounts_of_crimes
from utils.filters.crimes_filters import get_crimes_per_capita

def get_all_crimes(secretary, crime, city, initial_month, final_month, per_capita):
    # validate the params
    if secretary and secretary not in ['sp', 'df']:
        return "Parâmetro secretary inválido", 400

    if crime and crime not in valid_crimes_df and crime not in valid_crimes_sp:
        return "Parâmetro crime inválido", 400

    if (initial_month and final_month is None) or (final_month and initial_month is None):
        return "Parâmetro initial_month ou final_month inválido", 400

    valid_months = []
    if initial_month is not None and final_month is not None:
        valid_months = get_all_valid_months(initial_month, final_month)

    data = []
    if (secretary == "df" or secretary is None) and (crime in valid_crimes_df or crime is None):
        _data = db['crimes_df'].find(
            { '$and': [
                { 'cities.name': city } if city else {},
                { 'period': { '$in': valid_months } } if len(valid_months) > 0 else {},
            ] },
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [valid_crimes_df.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True,
            }
        )
        if initial_month is not None and final_month is not None:
            data.append(get_cumulative_amounts_of_crimes(list(_data), initial_month, final_month))
        else:
            data += list(_data)

        if per_capita:
            data = get_crimes_per_capita(data, 'Distrito Federal')
    if (secretary == "sp" or secretary is None) and (crime in valid_crimes_sp or crime is None):
        _data = db['crimes_sp'].find(
            { '$and': [
                { 'cities.name': city } if city else {},
                { 'period': { '$in': valid_months } } if len(valid_months) > 0 else {},
            ] },
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [valid_crimes_sp.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True
            }
        )
        if initial_month is not None and final_month is not None:
            data.append(get_cumulative_amounts_of_crimes(list(_data), initial_month, final_month))
        else:
            data += list(_data)

        if per_capita:
            data = get_crimes_per_capita(data, 'São Paulo')

    if city and data == []:
        return "Parâmetro cidade inválido", 400

    return data, 200
