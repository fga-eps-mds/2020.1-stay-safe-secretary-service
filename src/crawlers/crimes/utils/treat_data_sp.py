def get_cities_data_by_year(year, cities, cities_data):
    crimes_data_by_city = []
    for city in cities:
        crimes_data = {}
        crimes_data[city] = cities_data[city][year]
        crimes_data_by_city.append(crimes_data)

    return crimes_data_by_city