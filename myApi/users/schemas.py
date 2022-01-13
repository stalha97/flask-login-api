from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length, Email
from myApi.models import User

# This schema is used to validate the user form data


class UserSchema(Schema):
    username = fields.Str(required=True, valdiate=Length(max=20))
    email = fields.Email(required=True, valdiate=Length(max=120))
    password = fields.Str(required=True, valdiate=Length(max=60))

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)
