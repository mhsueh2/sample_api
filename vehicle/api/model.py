from api.dao import VehicleDAO


class Vehicle:

    BOOKED = 'booked'
    FREE = 'free'

    def __init__(self, vehicle):
        vehicle = vehicle.__dict__

        self.vehicle_id = int(vehicle.get('vehicle_id'))
        self.booking_status = Vehicle.BOOKED if vehicle.get('is_booked', False) else Vehicle.FREE
        self.key = vehicle.get('key', '')
        self.user_id = vehicle.get('user_id')


class VehicleModel:

    def get_vehicle_by_id(self, vehicle_id) -> object:
        dao = VehicleDAO()
        vehicle = dao.get_vehicle_by_id(vehicle_id)

        return Vehicle(vehicle)

    def start_booking(self, payload):
        vehicle = self.get_vehicle_by_id(payload['vehicle_id'])
        if vehicle.booking_status == Vehicle.BOOKED:
            raise LookupError

        dao = VehicleDAO()
        key = dao.request_key_from_middelware(payload['vehicle_id'])
        to_update = {'key': key, 'user_id': payload['user_id'], 'is_booked': True}

        # ROLLBACK operation if the DB update fails
        try:
            dao.update_vehicle_by_id(payload['vehicle_id'], to_update)
        except Exception:
            dao.delete_key_from_middleware(key)
            raise

        dao.session.commit()

    def end_booking(self, payload):
        vehicle = self.get_vehicle_by_id(payload['vehicle_id'])
        if vehicle.booking_status == Vehicle.FREE:
            raise LookupError('Vehicle has not been booked')

        # The addition of the user_id field ensures that booking termination is locked to its originator
        if vehicle.user_id != payload['user_id']:
            raise LookupError('Unmatched user')

        dao = VehicleDAO()
        to_update = {'key': str(), 'user_id': None, 'is_booked': False}

        dao.update_vehicle_by_id(payload['vehicle_id'], to_update)
        dao.delete_key_from_middleware(vehicle.key)

        # All interal server error exceptions are thrown at DAO level,
        # which ensures DB change will only be recorded upon successful operation
        dao.session.commit()

