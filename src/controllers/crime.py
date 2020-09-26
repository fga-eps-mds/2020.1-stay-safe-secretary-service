from database.db import db


def get_all_crimes(secretary, crime):
    # validate the params
    if (secretary and secretary not in ['sp', 'df']):
        return "Parâmetro secretary inválido", 400

    valid_crimes = ['Latrocinio', 'Roubo a Transeunte', 'Roubo de Veículo',
                    'Roubo de Residência', 'Estupro']
    if (crime and crime not in valid_crimes):
        return "Parâmetro crime inválido", 400

    # getting the data
    data = []
    if (secretary == "df" or secretary is None):
        _data = db['crimes_df'].find({}, {'_id': False})
        data += [data for data in _data]
    if (secretary == "sp" or secretary is None):
        _data = db['crimes_sp'].find({}, {'_id': False})
        data += [data for data in _data]

    # filtering the data
    for year in range(len(data)):
        for city in range(len(data[year]['cities'])):
            city_name = list(data[year]['cities'][city].keys())[0]
            data[year]['cities'][city][city_name] = \
                list(filter(lambda x:
                            (x['crime_nature'] == crime) if crime else True,
                            data[year]['cities'][city][city_name]))

    return data, 200
