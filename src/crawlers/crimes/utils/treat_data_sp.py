def get_city_data_by_month(annual_crimes_data, month):
    annual_city_data = []

    for crime in annual_crimes_data:
        crimes_data = {}
        crimes_data['nature'] = crime['nature']
        crimes_data['quantity'] = crime['quantities'][month]

        annual_city_data.append(crimes_data)

    return annual_city_data