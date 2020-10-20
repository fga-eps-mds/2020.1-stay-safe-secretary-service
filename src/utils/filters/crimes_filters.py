def get_cumulative_amounts_of_crimes(data, initial_month, final_month):
    new_data = data[0]
    new_data['period'] = f'{initial_month}-{final_month}'

    for i, _data in enumerate(data):
        if i > 0:
            for j, city in enumerate(_data['cities']):
                for k, crime in enumerate(city['crimes']):
                    new_data['cities'][j]['crimes'][k]['quantity'] += crime['quantity']

    return new_data