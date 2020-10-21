import unittest

from controllers import coordinates as controller
from database.db import db


class TestCoordinates(unittest.TestCase):
    def setUp(self):
        # getting the db size before tests
        _data = db['coordinates'].find({}, {'_id': False})
        self.data = list(_data)

        self.db_len = len(self.data)

    def test_get_coordinates_from_one_state(self):
        """
        Testing get coordinates from one state
        """
        result, status = controller.get_all_coordinates('sp')
        self.assertEqual(status, 200)
        new_db_len = len(result)
        self.assertEqual(new_db_len, self.db_len)

    def test_get_coordinates_from_invalid_state(self):
        """
        Testing get coordinates from invalid state
        """
        result, status = controller.get_all_coordinates("mt")

        self.assertEqual(status, 400)
        self.assertEqual(result, "Parâmetro state inválido")

    def test_try_get_all_coordinates(self):
        """
        Testing get all coordinates
        """
        result, status = controller.get_all_coordinates(None)
        self.assertEqual(status, 400)
        self.assertEqual(result, "Parâmetro state inválido")