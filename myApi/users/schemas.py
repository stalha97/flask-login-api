from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length, Email
from myApi.models import User


class UserSchema(Schema):
    class Meta:
        fields = ("username", "email", "password")

    # username = fields.Str(required=True, valdiate=Length(max=20))
    # email = fields.Email(required=True, valdiate=Length(max=120))
    # password = fields.Str(required=True, valdiate=Length(max=60))

    @post_load
    def create_user(self, data, **kwargs):
        # return User(username="",email="", password="")
        return User(**data)
