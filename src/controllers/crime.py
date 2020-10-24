from database.db import db

from utils.constants import VALID_CRIMES_DF, VALID_CRIMES_SP
from utils.valid_months import get_all_valid_months
from utils.amount_crimes import get_cumulative_amounts_of_crimes
from utils.amount_crimes import get_crimes_per_capita
from utils.amount_crimes import sort_crimes
from utils.validators.validate_filters import validade_crime_filters

def get_all_crimes(params, per_capita):
    # Validate the params
    error = validade_crime_filters(params, per_capita)
    if error:
        return error, 400

    secretary = params.get('secretary')
    crime = params.get('nature')
    city = params.get('city')
    initial_month = params.get('initial_month')
    final_month = params.get('final_month')

    if secretary == 'df':
        valid_crimes = VALID_CRIMES_DF
    elif secretary == 'sp':
        valid_crimes = VALID_CRIMES_SP

    valid_months = []
    quantity_months = 1
    if initial_month and final_month:
        valid_months = get_all_valid_months(initial_month, final_month)
        quantity_months = len(valid_months)

    data = []
    # Get data according to queries params
    if crime in valid_crimes or crime is None:
        collection_name = f'crimes_{secretary}'

        _data = db[collection_name].find(
            { '$and': [
                { 'cities.name': city } if city else {},
                { 'period': { '$in': valid_months } } if len(valid_months) > 0 else {},
            ] },
            { '_id': False, 'capture_data': True, 'period': True,
                'cities.crimes': { '$slice': [valid_crimes.index(crime), 1] } if crime else True,
                'cities': { '$elemMatch': { 'name': city } } if city else True,
            }
        )

        db_data = list(_data)
        if len(db_data) > 0:
            if quantity_months > 1:
                months_data = []
                cumulative_data = get_cumulative_amounts_of_crimes(db_data)
                cumulative_data['period'] = f'{initial_month}-{final_month}'

                months_data.append(cumulative_data)
                db_data = months_data

            if per_capita == '1':
                db_data = get_crimes_per_capita(db_data, secretary, quantity_months)

            # Sort the crimes in decreasing order of quantities.
            for _data in db_data:
                for city in _data['cities']:
                    city['crimes'].sort(reverse=True, key=sort_crimes)

            data += db_data
    else:
        return 'Crime não existente na secretaria.', 400

    return data, 200
