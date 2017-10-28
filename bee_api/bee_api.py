import decimal
import flask.json

from flask import Flask, jsonify, request

from flask_restful import Api
from flask_restless import ProcessingException
from flask_cors import CORS
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, MigrateCommand
from schema import *
from models import db


class DecJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(DecJSONEncoder, self).default(obj)


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.json_encoder = DecJSONEncoder


#api = Api(app)
CORS(app, resources=r'/api/*')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
stateProvince_schema = StateProvinceSchema()
stateProvinces_schema = StateProvinceSchema(many=True)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)
hive_schema = HiveSchema()
hives_schema = HiveSchema(many=True)
hiveData_schema = HiveDataSchema()
hiveDatas_schema = HiveDataSchema(many=True)

##### API #####

def add_country_helper(json_data):
    country = Country(name=json_data['name'],)
    db.session.add(country)
    db.session.commit()
    return country


@app.route('/countries')
def get_countries():
    results = Country.query.all()
    result = countries_schema.dump(results)
    return jsonify({'countries': result.data})


@app.route("/countries/<int:pk>")
def get_country(pk):
    try:
        country = Country.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Country could not be found."}), 400
    result = country_schema.dump(country)
    return jsonify({"countries": result.data})


@app.route("/countries/", methods=["POST"])
def new_country():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = country_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    if Country.query.filter_by(name=data['name']).first():
        raise ProcessingException(
            description='State, {}, already exists'.format(
                data['name']), code=409)
        return

    country = add_country_helper(data)
    result = country_schema.dump(Country.query.get(country.id))
    return jsonify({"message": "Created new Country.",
                    "Country": result.data})


@app.route('/stateprovinces')
def get_stateProvinces():
    stateprovinces = StateProvince.query.all()
    # Serialize the queryset
    result = stateProvinces_schema.dump(stateprovinces)
    return jsonify({'stateprovinces': result.data})


@app.route("/stateprovinces/<int:pk>")
def get_stateProvince(pk):
    try:
        stateProvince = StateProvince.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "State/Province could not be found."}), 400
    result = stateProvince_schema.dump(stateProvince)
    return jsonify({"stateprovinces": result.data})


@app.route("/stateprovinces/", methods=["POST"])
def new_stateprovinces():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = stateProvince_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    country = Country.query.filter_by(
        name=json_data['country']['name']).first()
    if country is None:
        country = Country(name=json_data['country']['name'])
        db.session.add(country)

    if StateProvince.query.filter_by(
        name=json_data['name'],
        abbreviation=json_data['abbreviation']).first():
            raise ProcessingException(
                description='State, {}, already exists'.format(
                    json_data['name']), code=409)
            return

    stateProvince = StateProvince(
        name = json_data['name'],
        abbreviation = json_data['abbreviation'],
        countryId = country.id
#        country = country
    )
    db.session.add(stateProvince)
    db.session.commit()
    result = StateProvince.query.get(stateProvince.id)
    result = stateProvince_schema.dump(StateProvince.query.get(stateProvince.id))
    return jsonify({"message": "Created new State/Province.",
                    "stateprovinces": result.data})


@app.route('/locations')
def get_locations():
    locations = Location.query.all()
    result = locations_schema.dump(locations)
    return jsonify({'locations': result.data})


@app.route("/locations/<int:pk>")
def get_location(pk):
    try:
        location = Location.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Location could not be found."}), 400
    result = location_schema.dump(location)
    return jsonify({"locations": result.data})


@app.route("/locations/", methods=["POST"])
def new_locations():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = location_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    stateProvince = StateProvince.query.filter_by(
        name = data['stateProvince']['id']
    )

    if stateProvince is None:
        country = Country.query.filter_by(
            name=data['stateprovince']['country']['name']
        )
        if country is None:
            country = Country(
                name=data['stateProvince']['country']['name'])
            db.session.add(country)
        stateProvince = StateProvince(
            name=data['stateprovince']['name'],
            abbreviation = data['stateprovince']['abbreviation'],
            country = country
        )

    if Location.query.filter_by(
        streetAddress=data['streetAddress'],
        city=data['city'],
        stateProvince=stateProvince).first():
        raise ProcessingException(
            description='Location, {}, {}, already exists'.format(
                data['streetAddress'], data['city']), code=409)
        return

    location = Location(
        streetAddress=data['streetAddress'],
        city=data['city'],
        stateProvince=stateProvince)

    db.session.add(location)
    db.session.commit()
    result = location_schema.dump(location.query.get(location.id))
    return jsonify({"message": "Created new Location.",
                    "locations": result.data})

"""
    country = Country.query.filter_by(name=data['country']['name']).first()
    if country is None:
        country = Country(name=data['country']['name'])
        db.session.add(country)

    if StateProvince.query.filter_by(
        name=data['name'],
        abbreviation=data['abbreviation']).first():
            raise ProcessingException(
                description='State, {}, already exists'.format(
                    data['name']), code=409)
            return

    stateProvince = StateProvince(
        name = data['name'],
        abbreviation = data['abbreviation'],
        country = country
    )
    db.session.add(stateProvince)
    db.session.commit()
    result = stateProvince_schema.dump(StateProvince.query.get(StateProvince.id))
    return jsonify({"message": "Created new State/Province.",
                    "State/Province": result.data})
"""


@app.route('/owners')
def get_owners():
    results = Owner.query.all()
    result = owners_schema.dump(results)
    return jsonify({'owners': result.data})


@app.route("/owners/<int:pk>")
def get_owner(pk):
    try:
        results = Owner.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Owner could not be found."}), 400
    result = owner_schema.dump(results)
    return jsonify({"owners": result.data})


@app.route('/hives')
def get_hives():
    results = Hive.query.all()
    result = hives_schema.dump(results)
    return jsonify({'hives': result.data})


@app.route("/hives/<int:pk>")
def get_hive(pk):
    try:
        results = Hive.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Hive could not be found."}), 400
    result = hive_schema.dump(results)
    return jsonify({"hives": result.data})


@app.route("/hivedata/", methods=["POST"])
def new_hivedata():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
    data, errors = hiveData_schema.load(json_data)
    if errors:
        return jsonify(errors), 422

    hiveId = Hive.query.filter_by(
            id=data['hive']['id']
        )

    if hiveId is None:
        return jsonify({'message': 'Invalid Hive Id'}), 400

    hiveData = HiveData(hiveId=data['hive']['id'],temperature=data['temperature'],
        humidity=data['humidity']
    )

    db.session.add(hiveData)
    db.session.commit()
    return jsonify({"message": "Created Hive Data Entry"})


@app.route("/hivedata/<int:pk>")
def get_hivedata_id(pk):
    try:
        results = HiveData.query.get(pk)
    except IntegrityError:
        return jsonify({"message": "Hive Data could not be found."}), 400
    result = hiveData_schema.dump(results)
    return jsonify({"hivedata": result.data})


@app.route("/hivedata")
def get_hivedata():
    try:
        results = HiveData.query.all()
    except IntegrityError:
        return jsonify({"message": "Hive Data could not be found."}), 400
    result = hiveDatas_schema.dump(results)
    return jsonify({"hivedata": result.data})


if __name__ == '__main__':
    app.run(host='0.0.0.0')