from marshmallow import Schema, fields, ValidationError, pre_load
from models import *


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class CountrySchema(Schema):
    stateProvinces = fields.Nested('StateProvinceSchema', many=True,
                        exclude=('country', ))

    class Meta:
        fields = ('id', 'name', 'stateProvinces')


class StateProvinceSchema(Schema):
    country = fields.Nested(CountrySchema, only=('id', 'name'),
                            exclude=('stateProvinces', ))
    location = fields.Nested('LocationSchema', many=True,
                            exclude=('statesProvince', ))

    class Meta:
        fields = ('id', 'name', 'abbreviation', 'country',
                  'location')


class LocationSchema(Schema):
    stateProvince = fields.Nested('StateProvinceSchema',
                        exclude=('location', ))

    class Meta:
        fields = ('id', 'streetAddress', 'city', 'stateProvince')


class OwnerSchema(Schema):
    location = fields.Nested(LocationSchema)
    hives = fields.Nested('HiveSchema', many=True,
                          exclude=('owner', ))
    fullName = fields.Method("format_name", dump_only=True)

    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'phoneNumber',
                   'fullName', 'location', 'hives')

    def format_name(self, owner):
        return "{} {}".format(owner.firstName, owner.lastName)


class HiveSchema(Schema):
    owner = fields.Nested(OwnerSchema)
    location = fields.Nested(LocationSchema)
    hiveData = fields.Nested('HiveDataSchema', many=True,
                        exclude=('hive', ))

    class Meta:
        fields = ('id', 'hiveData', 'owner', 'location', 'dateCreated',
                  'lastUpdate')

class HiveDataSchema(Schema):
    hive = fields.Nested(HiveSchema, exclude = ('stateProvinces',))

    class Meta:
        fields = ('id', 'hive', 'dateCreated', 'temperature', 'humidity')
