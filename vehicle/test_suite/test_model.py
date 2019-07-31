import unittest
from unittest.mock import MagicMock, patch

from api.model import VehicleModel, Vehicle


class MockedVehicleDB:

    def __init__(self):
        self.vehicle_id = 1
        self.is_booked = True
        self.key = 'mock'
        self.user_id = 1


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.vehicle_id = 1
        self.payload = {
            'vehicle_id': self.vehicle_id,
            'user_id': 1
        }
        self.mocked_db_obj = MockedVehicleDB()
        self.model = VehicleModel()

    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_get_vehicle_by_id(self, mocked_get):
        mocked_get.return_value = self.mocked_db_obj
        result = self.model.get_vehicle_by_id(self.vehicle_id)

        self.assertIsInstance(result, Vehicle)
        self.assertEqual(result.vehicle_id, self.mocked_db_obj.vehicle_id)
        self.assertEqual(result.user_id, self.mocked_db_obj.user_id)
        self.assertEqual(result.key, self.mocked_db_obj.key)
        self.assertEqual(result.booking_status, 'booked')

    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_start_booking_on_booked_vehicle(self, mocked_get):
        mocked_get.return_value = self.mocked_db_obj
        with self.assertRaises(LookupError):
            self.model.start_booking(self.payload)

    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_start_booking_on_booked_vehicle(self, mocked_get):
        mocked_get.return_value = self.mocked_db_obj
        with self.assertRaises(LookupError):
            self.model.start_booking(self.payload)

    @patch('api.dao.VehicleDAO.delete_key_from_middleware')
    @patch('api.dao.VehicleDAO.update_vehicle_by_id', MagicMock(side_effect=Exception))
    @patch('api.dao.VehicleDAO.request_key_from_middelware', MagicMock(return_value='key'))
    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_start_booking_deletes_key_on_db_failure(self, mocked_get, mocked_delete_key):
        self.mocked_db_obj.is_booked = False
        mocked_get.return_value = self.mocked_db_obj
        with self.assertRaises(Exception):
            self.model.start_booking(self.payload)
        mocked_delete_key.assert_called_once_with('key')

    @patch('api.dao.VehicleDAO.update_vehicle_by_id', MagicMock(return_value=None))
    @patch('api.dao.VehicleDAO.request_key_from_middelware', MagicMock(return_value='key'))
    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_start_booking_success(self, mocked_get):
        self.mocked_db_obj.is_booked = False
        mocked_get.return_value = self.mocked_db_obj
        self.model.start_booking(self.payload)

    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_end_booking_on_free_vehicle(self, mocked_get):
        self.mocked_db_obj.is_booked = False
        mocked_get.return_value = self.mocked_db_obj
        with self.assertRaises(LookupError):
            self.model.end_booking(self.payload)

    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_end_booking_on_invalid_user(self, mocked_get):
        self.mocked_db_obj.user_id = 4
        mocked_get.return_value = self.mocked_db_obj
        with self.assertRaises(LookupError):
            self.model.end_booking(self.payload)

    @patch('api.dao.VehicleDAO.delete_key_from_middleware')
    @patch('api.dao.VehicleDAO.update_vehicle_by_id')
    @patch('api.dao.VehicleDAO.get_vehicle_by_id')
    def test_end_booking_db_success(self, mocked_get, mocked_update, mocked_delete_key):
        mocked_get.return_value = self.mocked_db_obj
        self.model.end_booking(self.payload)

        mocked_update.assert_called_once_with(self.vehicle_id, {'key': str(), 'user_id': None, 'is_booked': False})
        mocked_delete_key.assert_called_once_with(self.mocked_db_obj.key)
