import datetime
#from marshmallow_jsonapi import Schema, fields
#from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,\
    Numeric, Boolean, create_engine

#from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

from sqlalchemy.orm import relationship

Base = declarative_base()
db = SQLAlchemy()


def init_app(app):
    """Initializes Flask app."""
    db.app = app
    db.init_app(app)
    return db


def create_tables(app):
    "Create tables, and return engine in case of further processing."
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class StateProvince(db.Model):
    __tablename__ = 'stateProvince'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    countryId = db.Column(db.Integer, ForeignKey('country.id'))
    country = db.relationship('Country', backref='stateProvinces')
    name = db.Column(db.String(200))
    abbreviation = db.Column(db.String(10))

    def __repr__(self):
        return self.name


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    streetAddress = db.Column(db.String(200))
    city = db.Column(db.String(200))
    stateProvinceId = db.Column(db.Integer, ForeignKey('stateProvince.id'))
    stateProvince = db.relationship('StateProvince', backref='location')

class Owner(db.Model):
    __tablename__ = 'owner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    passwd = db.Column(db.String(200))
    email = db.Column(db.String(400))
    phoneNumber = db.Column(db.String(20))
    locationId = db.Column(db.Integer, ForeignKey('location.id'))
    location = db.relationship('Location', backref='owner')


    def __repr__(self):
        return "{} {}".format(self.firstName, self.lastName)

#    @validates('email')
#    def validate_email(self, key, address):
#        assert '@' in address
#        return address


class Hive(db.Model):
    __tablename__ = "hive"
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, ForeignKey('owner.id'))
    owner = db.relationship('Owner', backref='hives')
# Hive location may differ from the location of the bee keeper
    locationId = db.Column(db.Integer, ForeignKey('location.id'))
    location = db.relationship('Location', backref='hives')
    dateCreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    lastUpdate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#    door_open = Column(Boolean, server_default=True)


class HiveData(db.Model):
    __tablename__ = "hiveData"
    id = db.Column(db.Integer, primary_key=True)
    hiveId = db.Column(db.Integer, ForeignKey('hive.id'))
    hive = db.relationship('Hive', backref='hiveData')
    dateCreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    temperature = db.Column(db.Numeric)
    humidity = db.Column(db.Numeric)
#    door_open = Column(Boolean, server_default=True)
