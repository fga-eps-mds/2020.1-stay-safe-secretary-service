import pandas as pd

crimes_nature = ('LATROCÍNIO', 'ROUBO A TRANSEUNTE', 'ROUBO DE VEÍCULO', 'ROUBO EM RESIDÊNCIA', 'ESTUPRO', 'TRÁFICO DE DROGAS')

def treat_extracted_data(filtered_crimes):
    city_data = []

    for key, value in filtered_crimes.items():
        type_crime = {}
        type_crime['crime_nature'] = key
        type_crime['quantity'] = int(float(value))

        city_data.append(type_crime)

    return city_data
    

def get_datas_from_excel(name, year):

    try:
        df_excel = pd.read_excel(f'./data/{str(year)}/{name}.xlsx', usecols=[i for i in range(1, 3)], index_col=0, skiprows=7, skipfooter=3)
        df_excel = df_excel.rename(columns={'Unnamed: 2': 'Total'}, inplace=False)

        crimes = dict(zip([str(crime) for crime in df_excel.index], [str(value[0]) for value in df_excel.values]))

        # Filter dictionary by keeping elements whose keys are in crime_nature list 
        filtered_crimes = dict(filter(lambda elem : elem[0] in crimes_nature, crimes.items()))

        city_data = treat_extracted_data(filtered_crimes)
    
        return city_data
    
    except FileNotFoundError:
        return []


def load_data(names_of_cities, year):
    cities_data = []
    for city_name in names_of_cities:
        crimes_data = {}
        city_data = get_datas_from_excel(city_name, year)
        crimes_data[city_name] = city_data

        cities_data.append(crimes_data)

    return cities_data