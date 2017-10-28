import os
import glob
import json
from flask_fixtures import FixturesMixin, load_fixtures
from flask_fixtures.loaders import JSONLoader
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from bee_api import app, db
import unittest
import tempfile


class BeeWebTestCase(unittest.TestCase):

    def setUp(self):
        db_name = 'testing_temp.db'
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_name)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing_temp.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.db_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),'..',db_name)
        fixture_files = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..','fixtures','*json')

        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            for fixture_file in glob.glob(fixture_files):
                fixtures = JSONLoader().load(fixture_file)
                load_fixtures(db, fixtures)


    def tearDown(self):
        db.session.remove()
        with app.app_context():
            db.drop_all()
            os.close(self.db_fd)
  #          os.unlink(app.config['DATABASE'])


    def test_get_all_countries(self):
        rv = self.app.get('/countries')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(len(json_resp['countries']), 3)
        self.assertEqual(json_resp['countries'][0]['name'], 'United States')
        self.assertEqual(json_resp['countries'][0]['id'], 1)

    def test_get_country(self):
        rv = self.app.get('/countries/2')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(len(json_resp),1)
        self.assertEqual(json_resp['countries']['name'], 'Canada')
        self.assertEqual(json_resp['countries']['id'], 2)

    def test_add_country(self):
        rv = self.app.post('/countries/',
                           content_type='application/json',
                           data=json.dumps(dict(name='West Germany')))

        self.assertEqual(rv.status_code, 200)

        rv = self.app.post('/countries/',
                           content_type='application/json',
                           data=json.dumps({'name':'West Germany'}))

        self.assertEqual(rv.status_code, 409)


    def test_get_all_statesprovinces(self):
        rv = self.app.get('/stateprovinces')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)

        self.assertEqual(len(json_resp['stateprovinces']), 50)
        self.assertEqual(json_resp['stateprovinces'][0]['name'], 'Alabama')
        self.assertEqual(json_resp['stateprovinces'][0]['country']['id'], 1)
        self.assertEqual(json_resp['stateprovinces'][0]['country']['name'],
                         'United States')
        self.assertEqual(json_resp['stateprovinces'][0]['abbreviation'], 'AL')

    def test_get_statesprovinces(self):
        rv = self.app.get('/stateprovinces/21')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)

        self.assertEqual(len(json_resp), 1)
        self.assertEqual(json_resp['stateprovinces']['name'], 'Massachusetts')
        self.assertEqual(json_resp['stateprovinces']['country']['id'],1)
        self.assertEqual(json_resp['stateprovinces']['abbreviation'], 'MA')
        self.assertEqual(json_resp['stateprovinces']['location'][0]['id'], 1)
        self.assertEqual(json_resp['stateprovinces']['location'][0]['city'],
                         'Boston')
        self.assertEqual(json_resp['stateprovinces']['location'][0]
                         ['streetAddress'],'123 Main St.')

    def test_add_stateprovinces(self):
        json_data = dict(name="Quebec", abbreviation="QC",
                     country=dict(name="Canada", id=2))
        rv = self.app.post('/stateprovinces/',
                           data = json.dumps(json_data),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(json_resp['stateprovinces']['abbreviation'], 'QC')
        self.assertEqual(json_resp['stateprovinces']['name'], 'Quebec')
        self.assertEqual(json_resp['stateprovinces']['country']['id'], 2)

        json_data = dict(name="Quebec", abbreviation="QC",
                     country=dict(name="Canada", id=2))

        rv = self.app.post('/stateprovinces/',
                           data = json.dumps(json_data),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 409)

#    def test_add_location(self):
#        rv = self.app.post('/locations/',
#                           content_type='application/json',
#                           data=json.dumps(dict(city='Hanover',
#                                streetAddress='84 Summer St.',
#                                stateprovince=dict(name='Massachusetts', id=21))))

 #       self.assertEqual(rv.status_code, 200)

    def test_get_all_locations(self):
        rv = self.app.get('/locations')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(json_resp['locations'][0]['city'], 'Boston')
        self.assertEqual(json_resp['locations'][0]['id'], 1)
        self.assertEqual(json_resp['locations'][0]['streetAddress'], '123 Main St.')

        json_resp = json.loads(rv.data)


    def test_get_locations(self):
        rv = self.app.get('/locations/1')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(json_resp['locations']['city'], 'Boston')
        self.assertEqual(json_resp['locations']['id'], 1)
        self.assertEqual(json_resp['locations']['streetAddress'], '123 Main St.')


    def test_get_owners(self):
        rv = self.app.get('/owners/1')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(json_resp['owners']['firstName'], 'Mickey')
        self.assertEqual(json_resp['owners']['lastName'], 'Mouse')
        self.assertEqual(json_resp['owners']['email'], 'mm@disney.com')
        self.assertEqual(json_resp['owners']['location']['city'], 'Boston')
        self.assertEqual(json_resp['owners']['location']['id'], 1)
        self.assertEqual(json_resp['owners']['location']['streetAddress'],
                         '123 Main St.')
        self.assertEqual(json_resp['owners']['phoneNumber'],
                         '7812175265')


    def test_add_hivedata(self):
        json_data = dict(humidity=10.5, temperature=78.5,
                     hive=dict(id=1))
        rv = self.app.post('/hivedata/',
                           data = json.dumps(json_data),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(json_resp['message'], 'Created Hive Data Entry')


if __name__ == '__main__':
    unittest.main()