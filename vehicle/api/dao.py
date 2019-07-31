import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

from api import app
from util.settings import SQLALCHEMY_DATABASE_URI, DB_SCHEMA, DB_TABLE

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class VehicleDB(db.Model):
    __tablename__ = DB_TABLE
    __table_args__ = {'schema': DB_SCHEMA}

    vehicle_id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(40))
    user_id = db.Column(db.Integer)
    is_booked = db.Column(db.Boolean, default=False)


class VehicleDAO:

    def __init__(self):
        self.session = db.session

    @staticmethod
    def get_vehicle_by_id(vehicle_id) -> object:
        try:
            result = VehicleDB.query.filter_by(vehicle_id=vehicle_id).first()
        except Exception as e:
            raise

        if not result:
            raise NoResultFound

        return result

    @staticmethod
    def update_vehicle_by_id(vehicle_id, to_update):
        try:
            VehicleDB.query.filter_by(vehicle_id=vehicle_id).update(to_update)
        except Exception as e:
            raise

    @staticmethod
    def request_key_from_middelware(vehicle_id) -> str:
        url = 'http://summon.mocklab.io/key/add/'
        body = {'vehicle_id': vehicle_id}

        try:
            response = requests.post(url=url, json=body)
            key = response.json()['key']
        except Exception:
            raise

        return key

    @staticmethod
    def delete_key_from_middleware(key):
        url = 'http://summon.mocklab.io/key/delete/'
        body = {'key': key}

        try:
            requests.post(url=url, json=body)
        except Exception:
            raise