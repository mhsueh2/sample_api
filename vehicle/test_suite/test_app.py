import json
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm.exc import NoResultFound

from api.app import app


class MockedVehicle:

    def __init__(self):
        self.vehicle_id = 1
        self.booking_status = 'booked'
        self.key = 'mock'
        self.user_id = 1


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.post_headers = {'Content-Type': 'application/json'}

    @patch('api.app.Schema.vehicle_id', MagicMock(side_effect=Exception))
    def test_get_vehicle_invalid_vehicle_id(self):
        response = self.app.get("/vehicle/1")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Invalid vehicle_id")

    @patch('api.app.VehicleModel.get_vehicle_by_id', MagicMock(side_effect=Exception))
    def test_get_vehicle_internal_server_error(self):
        response = self.app.get("/vehicle/1")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['message'], "Internal server error")

    @patch('api.app.VehicleModel.get_vehicle_by_id', MagicMock(side_effect=NoResultFound))
    def test_get_vehicle_not_found(self):
        response = self.app.get("/vehicle/1")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "Vehicle does not exist")

    @patch('api.app.VehicleModel.get_vehicle_by_id')
    def test_get_vehicle_success(self, mocked_method):
        vehicle_obj = MockedVehicle()
        mocked_method.return_value = vehicle_obj

        response = self.app.get("/vehicle/1")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, vehicle_obj.__dict__)

    @patch('api.app.Schema.booking', MagicMock(side_effect=Exception))
    def test_post_booking_invalid_payload(self):
        response = self.app.post(
            "/start_booking",
            data=json.dumps({'bacon': 'eggs'}),
            headers=self.post_headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Invalid payload")

    @patch('api.app.Schema.booking', MagicMock(return_value={'test': 'test'}))
    @patch('api.app.VehicleModel.start_booking', MagicMock(side_effect=Exception))
    def test_post_booking_internal_server_error(self):
        response = self.app.post(
            "/start_booking",
            data=json.dumps({'bacon': 'eggs'}),
            headers=self.post_headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['message'], "Internal server error")

    @patch('api.app.Schema.booking', MagicMock(return_value={'test': 'test'}))
    @patch('api.app.VehicleModel.start_booking', MagicMock(side_effect=NoResultFound))
    def test_post_booking_vehicle_does_not_exist(self):
        response = self.app.post(
            "/start_booking",
            data=json.dumps({'bacon': 'eggs'}),
            headers=self.post_headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "Vehicle does not exist")

    @patch('api.app.Schema.booking', MagicMock(return_value={'test': 'test'}))
    @patch('api.app.VehicleModel.start_booking', MagicMock(side_effect=LookupError))
    def test_post_booking_vehicle_unaval(self):
        response = self.app.post(
            "/start_booking",
            data=json.dumps({'bacon': 'eggs'}),
            headers=self.post_headers)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Bad request")

    @patch('api.app.Schema.booking')
    @patch('api.app.VehicleModel.start_booking')
    def test_post_booking_vehicle_success(self, mocked_command, mocked_schema):
        expected = mocked_schema.return_value = {'test': 'bacon'}
        response = self.app.post(
            "/start_booking",
            data=json.dumps({'bacon': 'eggs'}),
            headers=self.post_headers)
        mocked_command.assert_called_once_with(mocked_schema.return_value)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, expected)

    @patch('api.app.Schema.booking')
    @patch('api.app.VehicleModel.end_booking')
    def test_post_end_booking_vehicle_success(self, mocked_command, mocked_schema):
        expected = mocked_schema.return_value = {'test': 'bacon'}
        response = self.app.post(
            "/end_booking",
            data=json.dumps({'bacon': 'eggs'}),
            headers=self.post_headers)
        mocked_command.assert_called_once_with(mocked_schema.return_value)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, expected)
