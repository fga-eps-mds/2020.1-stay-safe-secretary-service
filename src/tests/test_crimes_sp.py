import unittest

from controllers import crimes_sp as controller
from database.db import db


class TestCrime(unittest.TestCase):
    def setUp(self):
        # getting the db size before tests
        _data = db['crimes_sp'].find({}, {'_id': False})
        self.data_sp = list(_data)

        self.db_sp_len = len(self.data_sp)

    def tearDown(self):
        new_db_sp_len = len(self.data_sp)

        self.assertEqual(new_db_sp_len, self.db_sp_len)

    def test_get_all_crimes_from_sp_secretary(self):
        """
        Testing get crimes from sp secretary
        """
        result, status = controller.get_all_crimes_sp({}, None)

        self.assertEqual(status, 200)
        self.assertEqual(len(result), self.db_sp_len)

    def test_get_crimes_by_crime_nature(self):
        """
        Testing get crimes by the crime nature
        """
        result, status = controller.get_all_crimes_sp({
            'crime': 'Outros Roubos' }, None)

        self.assertEqual(status, 200)

        if self.db_sp_len > 0:
            for city in range(len(result[0]['cities'])):
                self.assertEqual(
                    result[0]['cities'][city]['crimes'][0]['nature'],
                    'Outros Roubos')

    def test_get_crimes_by_crime_of_another_secretary(self):
        """
        Testing get crimes by an crime nature existing only in another secretary
        """
        result, status = controller.get_all_crimes_sp({
                'crime': 'Furto a Transeunte' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result, "Parâmetro crime inválido.")

    def test_get_crimes_from_one_city(self):
        """
        Testing get crimes from one city of sp
        """
        result, status = controller.get_all_crimes_sp({
            'city': 'Adamantina' }, None)

        self.assertEqual(status, 200)

        if self.db_sp_len > 0:
            for city in result:
                self.assertEqual(city['cities'][0]['name'], 'Adamantina')

    def test_get_crimes_from_one_invalid_city(self):
        """
        Testing get crimes from one city out of sp
        """
        result, status = controller.get_all_crimes_sp({
            'city': 'Brasília' }, None)

        self.assertEqual(status, 200)
        self.assertEqual(result, [])

    def test_get_crimes_by_valid_period(self):
        """
        Testing get crimes by valid period
        """
        result, status = controller.get_all_crimes_sp({
            'initial_month': '1/2019', 'final_month': '12/2019' }, None)

        self.assertEqual(status, 200)

        if self.db_sp_len > 0:
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['period'], '1/2019-12/2019')

    def test_get_crimes_by_invalid_month(self):
        """
        Testing get crimes by invalid month
        """
        result, status = controller.get_all_crimes_sp({
            'initial_month': '0/2019', 'final_month': '12/2019' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month/final_month inválidos.')

    def test_get_crimes_by_invalid_year(self):
        """
        Testing get crimes by invalid year
        """
        result, status = controller.get_all_crimes_sp({
            'initial_month': '1/2000', 'final_month': '12/2000' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month/final_month inválidos.')

    def test_get_crimes_by_higher_initial_month(self):
        """
        Testing get crimes by higher initial_month
        """
        result, status = controller.get_all_crimes_sp({
            'initial_month': '3/2020', 'final_month': '10/2019' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month/final_month inválidos.')

    def test_get_crimes_with_only_one_period(self):
        """
        Testing get crimes with only one period
        """
        result, status = controller.get_all_crimes_sp({
            'final_month': '12/2019' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month e final_month devem ser passados juntos.')

    def test_get_crimes_per_capita(self):
        """
        Testing get crimes per capita
        """
        result, status = controller.get_all_crimes_sp({
            'initial_month': '1/2019', 'final_month': '12/2019' }, per_capita='1')

        self.assertEqual(status, 200)

        if self.db_sp_len > 0:
            for city in result[0]['cities']:
                for crime in city['crimes']:
                    self.assertTrue(1 <= crime['classification'] <= 6)
