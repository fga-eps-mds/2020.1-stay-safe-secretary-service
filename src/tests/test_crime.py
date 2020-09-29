import unittest

from controllers import crime as controller
from database.db import db


class TestCrime(unittest.TestCase):
    def setUp(self):
        # getting the db size before tests
        _data = db['crimes_df'].find({}, {'_id': False})
        self.data_df = [data for data in _data]
        _data = db['crimes_sp'].find({}, {'_id': False})
        self.data_sp = [data for data in _data]

        self.db_df_len = len(self.data_df)
        self.db_sp_len = len(self.data_sp)
        self.db_len = self.db_df_len + self.db_sp_len

    def tearDown(self):
        new_db_df_len = len(self.data_df)
        new_db_sp_len = len(self.data_sp)
        new_db_len = new_db_df_len + new_db_sp_len
        self.assertEqual(new_db_df_len, self.db_df_len)
        self.assertEqual(new_db_sp_len, self.db_sp_len)
        self.assertEqual(new_db_len, self.db_len)

    def test_get_all_crimes(self):
        """
        Testing get all crimes
        """
        result, status = controller.get_all_crimes(None, None)
        self.assertEqual(status, 200)
        new_db_len = len(result)
        self.assertEqual(new_db_len, self.db_len)

    def test_get_crimes_from_one_secretary(self):
        """
        Testing get crimes from only one secretary
        """
        secretarys = ['df', 'sp']
        for secretary in secretarys:
            result, status = controller.get_all_crimes(secretary, None)
            self.assertEqual(status, 200)
            new_db_secretary_len = len(result)
            if (secretary == 'df'):
                self.assertEqual(new_db_secretary_len, self.db_df_len)
            else:
                self.assertEqual(new_db_secretary_len, self.db_sp_len)

    def test_get_crimes_by_crime_nature(self):
        """
        Testing get crimes by the crime nature
        """
        result, status = controller.get_all_crimes(None, "Roubo a Transeunte")
        self.assertEqual(status, 200)
        # self.assertEqual(result[0]['cities'][9]['Gama'][0]['crime_nature'],
        #                 "Roubo a Transeunte")
