import sys, os
from flask import jsonify, request, make_response
from flask_restful import Api, Resource
from sqlalchemy.orm.exc import NoResultFound

sys.path.insert(1, os.path.realpath(os.path.pardir))
from api import app
from api.model import VehicleModel
from util.schema import Schema

api = Api(app)


class Vehicle(Resource):

    def get(self, vehicle_id):
        try:
            params = Schema.vehicle_id({'vehicle_id': vehicle_id})
        except Exception as e:
            return make_response(jsonify(message='Invalid vehicle_id', error=str(e)), 400)

        model = VehicleModel()
        try:
            result = model.get_vehicle_by_id(params['vehicle_id'])
        except NoResultFound as e:
            return make_response(jsonify(message='Vehicle does not exist', error=str(e)), 404)
        except Exception as e:
            return make_response(jsonify(message='Internal server error', error=str(e)), 500)

        return result.__dict__, 200


class Booking(Resource):

    def __init__(self, model=VehicleModel()):
        self.model = model
        self.booking_command = None

    def post(self):
        payload = request.get_json()
        try:
            payload = Schema.booking(payload)
        except Exception as e:
            return make_response(jsonify(message='Invalid payload', error=str(e)), 400)

        try:
            self.booking_command(payload)
        except LookupError as e:
            return make_response(jsonify(message='Bad request', error=str(e)), 400)
        except NoResultFound as e:
            return make_response(jsonify(message='Vehicle does not exist', error=str(e)), 404)
        except Exception as e:
            return make_response(jsonify(message='Internal server error', error=str(e)), 500)

        return payload, 200


class StartBooking(Booking):

    def __init__(self):
        super().__init__()
        self.booking_command = self.model.start_booking


class EndBooking(Booking):

    def __init__(self):
        super().__init__()
        self.booking_command = self.model.end_booking


api.add_resource(Vehicle, '/vehicle/<string:vehicle_id>')
api.add_resource(StartBooking, '/start_booking')
api.add_resource(EndBooking, '/end_booking')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
