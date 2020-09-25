from database.db import db
from utils.formatters import get_row_dict
from settings import logger
from pymongo import MongoClient
import os


def get_all_crimes(secretary, crime):
    data_df = []
    data_sp = []
    if (secretary == "df" or secretary == None):
        _data = db['crimes_df'].find()
        data_df = [data for data in _data]
    if (secretary == "sp" or secretary == None):
        _data = db['crimes_sp'].find()
        data_sp = [data for data in _data]

    for year in range(len(data_df)):
        data_df[year].pop('_id', None)
        for city in range(len(data_df[year]['cities'])):
            city_name = list(data_df[year]['cities'][city].keys())[0]
            data_df[year]['cities'][city][city_name] = list(filter(lambda x: (x['crime_nature'] == crime) if crime else True, data_df[year]['cities'][city][city_name]))
    
    for year in range(len(data_sp)):
        data_sp[year].pop('_id', None)
        for city in range(len(data_sp[year]['cities'])):
            city_name = list(data_sp[year]['cities'][city].keys())[0]
            data_sp[year]['cities'][city][city_name] = list(filter(lambda x: (x['crime_nature'] == crime) if crime else True, data_sp[year]['cities'][city][city_name]))
    
    return { 'df': data_df, 'sp': data_sp }, 200