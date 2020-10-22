from database.db import db

from utils.constants import VALID_CRIMES_DF, VALID_CRIMES_SP
from utils.valid_months import get_all_valid_months
from utils.amount_crimes import get_cumulative_amounts_of_crimes
from utils.amount_crimes import get_crimes_per_capita
from utils.amount_crimes import sort_crimes
from utils.validators.validate_filters import validade_crime_filters

def get_all_crimes(params, per_capita):
    # validate the params
    error = validade_crime_filters(params, per_capita)
    if error:
        return error, 400

    secretary = params.get('secretary')
    crime = params.get('crime')
    city = params.get('city')
    initial_month = params.get('initial_month')
    final_month = params.get('final_month')

    valid_months = []
    quantity_months = 1

    if initial_month and final_month:
        valid_months = get_all_valid_months(initial_period=initial_month,
            final_period=final_month)

        quantity_months = len(valid_months)

    data = []
    if (secretary == "df" or secretary is None) and (crime in VALID_CRIMES_DF or crime is None):
        _data = db['crimes_df'].find(
            { '$and': [
                { 'cities.name': city } if city else {},
                { 'period': { '$in': valid_months } } if len(valid_months) > 0 else {},
            ] },
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [VALID_CRIMES_DF.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True,
            }
        )

        data_df = list(_data)
        if len(data_df) > 0:
            if len(valid_months) > 0:
                months_data = []
                cumulative_data = get_cumulative_amounts_of_crimes(data_df)
                if quantity_months > 1:
                    cumulative_data['period'] = f'{initial_month}-{final_month}'

                months_data.append(cumulative_data)
                data_df = months_data

            if per_capita == '1':
                data_df = get_crimes_per_capita(data_df, 'df', quantity_months)

            for _data in data_df:
                for city in _data['cities']:
                    city['crimes'].sort(reverse=True, key=sort_crimes)

        if data_df != []:
            data += data_df

    if (secretary == "sp" or secretary is None) and (crime in VALID_CRIMES_SP or crime is None):
        _data = db['crimes_sp'].find(
            { '$and': [
                { 'cities.name': city } if city else {},
                { 'period': { '$in': valid_months } } if len(valid_months) > 0 else {},
            ] },
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [VALID_CRIMES_SP.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True
            }
        )

        data_sp = list(_data)
        if len(data_sp) > 0:
            if len(valid_months) > 0:
                months_data = []
                cumulative_data = get_cumulative_amounts_of_crimes(data_sp)
                if quantity_months > 1:
                    cumulative_data['period'] = f'{initial_month}-{final_month}'

                months_data.append(cumulative_data)
                data_sp = months_data

            if per_capita == '1':
                data_sp = get_crimes_per_capita(data_sp, 'sp', quantity_months)

            for _data in data_sp:
                for city in _data['cities']:
                    city['crimes'].sort(reverse=True, key=sort_crimes)

        if data_sp != []:
            data += data_sp

    return data, 200
