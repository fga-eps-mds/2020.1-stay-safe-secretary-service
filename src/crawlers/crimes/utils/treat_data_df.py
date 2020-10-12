"""
Functions to treat the DF data
"""
import pandas as pd

from utils.handle_folders import delete_file
from utils.crimes_nature import crimes_nature_df

def treat_extracted_data(filtered_crimes):
    """
    Create the array of crimes according to the architecture document.
    """
    crimes = []
    for key, value in filtered_crimes.items():
        type_crime = {}
        type_crime['nature'] = crimes_nature_df[key]
        type_crime['quantity'] = int(float(value))

        crimes.append(type_crime)

    return crimes


def get_data_from_excel(city_name):
    """
    Open the annual excel of a city, get the monthly data,
    treat them and return the annual data to the pipeline.
    """
    try:
        excel_table = pd.read_excel(
            f'./data/{city_name}.xlsx',
            usecols=range(1, 15),
            index_col=0,
            skiprows=7,
            skipfooter=3
        )

        annual_city_data = []
        for month in range(1, 13):
            # Create a dictionary following the pattern: {'crime_nature': quantity}
            crimes = dict(zip(
                [str(crime) for crime in excel_table.index],
                [str(value[month]) for value in excel_table.values]
            ))

            # Filter crimes by keeping elements whose keys are in crimes_nature_df list
            filtered_crimes = dict(filter(
                lambda elem : elem[0] in crimes_nature_df.keys(), crimes.items()
            ))

            monthly_city_data = treat_extracted_data(filtered_crimes)

            annual_city_data.append(monthly_city_data)

        # Delete the downloaded file
        delete_file(f'data/', f'{city_name}.xlsx')
        
        return annual_city_data

    except FileNotFoundError:
        return []
