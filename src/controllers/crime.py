from database.db import db


def get_all_crimes(secretary, crime):
    # validate the params
    if (secretary and secretary not in ['sp', 'df']):
        return "Parâmetro secretary inválido", 400

    if secretary == 'df':
        valid_crimes = ['Latrocínio', 'Roubo a Transeunte', 'Roubo de Veículo', 
                'Roubo de Residência', 'Estupro', 'Furto de Veículo', 'Furto a Transeunte']
    elif secretary == 'sp':
        valid_crimes = ['Latrocínio', 'Roubo de Veículo', 'Estupro', 
                'Furto de Veículo', 'Outros Roubos', 'Outros Furtos']
    
    if (crime and crime not in valid_crimes):
        return "Parâmetro crime inválido", 400

    # getting the data
    data = []
    if (secretary == "df" or secretary is None):
        _data = db['crimes_df'].find({}, {'_id': False})
        data += list(_data)
    if (secretary == "sp" or secretary is None):
        _data = db['crimes_sp'].find({}, {'_id': False})
        data += list(_data)

    # filtering the data
    for monthly_data in data:
        for city in monthly_data['cities']:
            city['crimes'] = \
                list(filter(lambda x:
                        (x['nature'] == crime) if crime else True,
                        city['crimes']))

    return data, 200
