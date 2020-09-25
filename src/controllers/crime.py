from database.db import db
from utils.formatters import get_row_dict
from settings import logger
from pymongo import MongoClient
import os


def get_all_crimes(secretary, crime):
    filters = {}
    if (crime):
        filters['crime_nature'] = crime
    if (secretary == "df" or secretary == None):
        _data = db['crimes_df'].find()
        data = [data for data in _data]
        for i in data:
            i.pop('_id', None)
            # for j in i['cities']:
            #     filter(lambda x: x['crime_nature'] == "Roubo a Transeunte", j)

    return data, 200