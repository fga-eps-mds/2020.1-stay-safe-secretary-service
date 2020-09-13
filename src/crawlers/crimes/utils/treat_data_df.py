"""
Functions to treat the DF data
"""
import pandas as pd
from utils.handle_folders import delete_file

crimes_nature = {
    'LATROCÍNIO': "Latrocinio",
    'ROUBO A TRANSEUNTE': 'Roubo a Transeunte',
    'ROUBO DE VEÍCULO': 'Roubo de Veiculo',
    'ROUBO EM RESIDÊNCIA': 'Roubo de Residencia',
    'ESTUPRO': 'Estupro',
    'TRÁFICO DE DROGAS': 'Trafico de Entorpecentes',
}

def treat_extracted_data(filtered_crimes):
    """
    Create the object with crimes nature quantity.
    """
    city_data = []

    for key, value in filtered_crimes.items():
        type_crime = {}
        type_crime['crime_nature'] = crimes_nature[key]
        type_crime['quantity'] = int(float(value))

        city_data.append(type_crime)

    return city_data


def get_datas_from_excel(name, year):
    """
    Open the excel and treating the table according
    to architecture document.
    """
    try:
        df_excel = pd.read_excel(
            f'./data/{str(year)}/{name}.xlsx',
            usecols=range(1, 3),
            index_col=0,
            skiprows=7,
            skipfooter=3
        )
        df_excel = df_excel.rename(columns={'Unnamed: 2': 'Total'}, inplace=False)

        crimes = dict(zip(
            [str(crime) for crime in df_excel.index],
            [str(value[0]) for value in df_excel.values]
        ))

        delete_file(f'data/{str(year)}', f'{name}.xlsx')

        # Filter dictionary by keeping elements whose keys are in crime_nature list
        filtered_crimes = dict(filter(
            lambda elem : elem[0] in crimes_nature.keys(), crimes.items()
        ))

        city_data = treat_extracted_data(filtered_crimes)

        return city_data

    except FileNotFoundError:
        return []


def load_data(names_of_cities, year):
    """
    Interating at DF cities list.
    """
    cities_data = []
    for city_name in names_of_cities:
        crimes_data = {}
        city_data = get_datas_from_excel(city_name, year)
        crimes_data[city_name] = city_data

        cities_data.append(crimes_data)

    return cities_data
