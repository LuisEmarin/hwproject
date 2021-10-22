from os import name
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin, login_manager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()

login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    flight = db.relationship('Flight', backref= 'owner', lazy = True)


    def __init__(self,email, password,token= '', id='') -> None:
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)


class Flight(db.Model):
    id = db.Column(db.String, primary_key=True)
    departsin_landsin = db.Column(db.String(200), nullable = True)
    flight_duration = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    cost_of_flight = db.Column(db.Numeric(precision= 10, scale=2))
    plane_series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, departsin_landsin, flight_duration, max_speed, cost_of_flight, plane_series, user_token, id = ''):
        self.id = self.set_id()
        self.departsin_landsin = departsin_landsin
        self.flight_duration = flight_duration
        self.max_speed = max_speed
        self.cost_of_flight = cost_of_flight
        self.plane_series = plane_series
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

class FlightSchema(ma.Schema):
    class Meta:
        fields = ['id', 'departsin_landsin', 'flight_duration', 'max_speed',  'cost_of_flight', 'plane_series']

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)
