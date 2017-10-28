from flask import jsonify
from flask.ext.restful import Resource
from models import Country, Location, State_Province

#Parser arguments that Flask-Restful will check for
#parser = reqparse.RequestParser()
#parser.add_argument('first_name', type=str, required=True, help="First Name Cannot Be Blank")
#parser.add_argument('last_name', type=str, required=True, help="Last Name Cannot Be Blank")
#parser.add_argument('email', type=str, required=True, help="Email Cannot Be Blank")

class LocationAPI(Resource):
    def get(self, id):
        e = Location.query.filter(Location.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def get(self):
#        e = User.query.all()
#        results = []
#        for row in User.query.all():
#            results.append(row.as_dict())
#        return results
        return jsonify(data=[Location.json for location in Location.query])

    def put(self, id):
        o = Location()
        o.first_name = args["first_name"]
        o.last_name = args["last_name"]
        o.email = args["email"]

        try:
            db_session.add(o)
            db_session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500

        return o.as_dict(), 201

    def delete(self, id):
        pass


class CountryAPI(Resource):
    def get(self, id):
        e = Country.query.filter(Country.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def get(self):
        return jsonify(data=[Country.json for country in Country.query])

    def put(self, id):
        pass

    def delete(self, id):
        pass
