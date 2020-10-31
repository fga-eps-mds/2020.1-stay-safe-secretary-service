import json

from utils.constants import ANNUAL_CRIMES_RANGE

def get_cumulative_amounts_of_crimes(data):
    for i, _data in enumerate(data):
        if i > 0:
            for j, city in enumerate(_data['cities']):
                for k, crime in enumerate(city['crimes']):
                    data[0]['cities'][j]['crimes'][k]['quantity'] += crime['quantity']

    return data[0]

def get_crimes_per_capita(data, secretary, months):
    population_data = open('static_data/populationData.json',)
    population_data = json.load(population_data)

    populations = list(filter(lambda state: state['state'] == secretary,
        population_data['populations']))

    for _data in data:
        for city in _data['cities']:
            for crime in city['crimes']:
                city_data = list(filter(
                    lambda x: x['name'] == city['name'], populations[0]['cities']))
                if city_data != []:
                    crime['quantity'] = (crime['quantity'] / city_data[0]['population']) * 100
                    crime['classification'] = get_classification(crime, secretary, months)

    return data

def get_classification(crime, secretary, months):
    """
    The classification is calculated according with the quantity of months of the data.
    """

    annual_state_crimes_range = list(
        filter(lambda state: state['state'] == secretary, ANNUAL_CRIMES_RANGE))[0]

    for index in range(0, 5):
        if crime['quantity'] <= months / 12 * \
                annual_state_crimes_range['crimes_range'][crime['nature']][index]:
            return index + 1

    return 6

def sort_crimes(crime):
    return crime['quantity']
