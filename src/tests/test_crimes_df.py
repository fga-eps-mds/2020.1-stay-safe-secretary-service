import unittest

from controllers import crimes_df as controller
from database.db import db


class TestCrime(unittest.TestCase):
    def setUp(self):
        # getting the db size before tests
        _data = db['crimes_df'].find({}, {'_id': False})
        self.data_df = list(_data)

        self.db_df_len = len(self.data_df)

    def tearDown(self):
        new_db_df_len = len(self.data_df)

        self.assertEqual(new_db_df_len, self.db_df_len)

    def test_get_all_crimes_from_df_secretary(self):
        """
        Testing get crimes from df secretary
        """
        result, status = controller.get_all_crimes_df({}, None)

        self.assertEqual(status, 200)
        self.assertEqual(len(result), self.db_df_len)

    def test_get_crimes_from_invalid_secretary(self):
        """
        Testing get crimes from one invalid secretary
        """
        result, status = controller.get_all_crimes_df({
            'secretary': 'mt' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result, "Parâmetro secretary inválido.")

    def test_get_crimes_by_crime_nature(self):
        """
        Testing get crimes by the crime nature
        """
        result, status = controller.get_all_crimes_df({
            'crime': 'Roubo a Transeunte' }, None)

        self.assertEqual(status, 200)
        for city in range(len(result[0]['cities'])):
            self.assertEqual(
                result[0]['cities'][city]['crimes'][0]['nature'],
                'Roubo a Transeunte')

    def test_get_crimes_by_invalid_crime_nature(self):
        """
        Testing get crimes by an invalid crime nature
        """
        result, status = controller.get_all_crimes_df({
                'crime': 'Roubo a Carga' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result, "Parâmetro crime inválido.")

    def test_get_crimes_by_crime_of_another_secretary(self):
        """
        Testing get crimes by an crime nature existing only in another secretary
        """
        result, status = controller.get_all_crimes_df({
                'crime': 'Outros Furtos' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result, "Parâmetro crime inválido.")

    def test_get_crimes_from_one_city(self):
        """
        Testing get crimes from one city of df
        """
        result, status = controller.get_all_crimes_df({
            'city': 'Águas Claras' }, None)

        self.assertEqual(status, 200)

        for city in result:
            self.assertEqual(city['cities'][0]['name'], 'Águas Claras')

    def test_get_crimes_from_one_invalid_city(self):
        """
        Testing get crimes from one city out of df
        """
        result, status = controller.get_all_crimes_df({
            'city': 'Adamantina' }, None)

        self.assertEqual(status, 200)
        self.assertEqual(result, [])

    def test_get_crimes_by_valid_period(self):
        """
        Testing get crimes by valid period
        """
        result, status = controller.get_all_crimes_df({
            'initial_month': '8/2019', 'final_month': '3/2020' }, None)

        self.assertEqual(status, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['period'], '8/2019-3/2020')

    def test_get_crimes_by_invalid_month(self):
        """
        Testing get crimes by invalid month
        """
        result, status = controller.get_all_crimes_df({
            'initial_month': '1/2019', 'final_month': '13/2019' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month/final_month inválidos.')

    def test_get_crimes_by_invalid_year(self):
        """
        Testing get crimes by invalid year
        """
        result, status = controller.get_all_crimes_df({
            'initial_month': '1/20', 'final_month': '12/20' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month/final_month inválidos.')

    def test_get_crimes_by_higher_initial_month(self):
        """
        Testing get crimes by higher initial_month
        """
        result, status = controller.get_all_crimes_df({
            'initial_month': '12/2019', 'final_month': '1/2019' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month/final_month inválidos.')

    def test_get_crimes_with_only_one_period(self):
        """
        Testing get crimes with only one period
        """
        result, status = controller.get_all_crimes_df({
            'initial_month': '1/2019' }, None)

        self.assertEqual(status, 400)
        self.assertEqual(result,
            'Parâmetros initial_month e final_month devem ser passados juntos.')

    def test_get_crimes_per_capita(self):
        """
        Testing get crimes per capita
        """
        result, status = controller.get_all_crimes_df({}, per_capita='1')

        self.assertEqual(status, 200)

        for period in result:
            for city in period['cities']:
                for crime in city['crimes']:
                    self.assertTrue(1 <= crime['classification'] <= 6)

    def test_get_crimes_invalid_per_capita(self):
        """
        Testing get crimes with only one period
        """
        result, status = controller.get_all_crimes_df({}, per_capita='5')

        self.assertEqual(status, 400)
        self.assertEqual(result, 'Parâmetro per_capita deve ser 1.')
