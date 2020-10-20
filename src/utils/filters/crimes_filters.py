import json

def get_cumulative_amounts_of_crimes(data, initial_month, final_month):
    new_data = data[0]
    new_data['period'] = f'{initial_month}-{final_month}'

    for i, _data in enumerate(data):
        if i > 0:
            for j, city in enumerate(_data['cities']):
                for k, crime in enumerate(city['crimes']):
                    new_data['cities'][j]['crimes'][k]['quantity'] += crime['quantity']

    return new_data

def get_crimes_per_capita(data, secretary):
    populationData = open('static_data/populationData.json',)
    populationData = json.load(populationData)

    populations = list(filter(lambda state: state['state'] == secretary, populationData['populations']))

    for _data in data:
        for city in _data['cities']:
            for crime in city['crimes']:
                city_data = list(filter(lambda x: x['name'] == city['name'], populations[0]['cities']))
                if city_data != []:
                    crime['quantity'] = crime['quantity'] / (city_data[0]['population']/10)

    return data