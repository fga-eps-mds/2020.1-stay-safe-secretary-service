from database import db
from utils.formatters import get_row_dict
from settings import logger
from pymongo import MongoClient
import os


def get_all_crimes(secretary, crime):
    result = db.get_all()
    
    return result, 200