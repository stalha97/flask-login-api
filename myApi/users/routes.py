from flask import request, Blueprint, session, jsonify
from marshmallow.exceptions import ValidationError
from myApi import db
from myApi.models import User
from myApi.users.schemas import UserSchema
from myApi.users.utils import user_exists

from webargs import fields, validate
from webargs.flaskparser import use_args


users = Blueprint("users", __name__)

user_schema = UserSchema()


# Return validation errors as JSON
@users.errorhandler(422)
@users.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages.get("json")}), err.code, headers
    else:
        return jsonify({"errors": messages.get("json")}), err.code


# Testing Marshmallow, and validations
"""
my_user_dict = {"email": "talha@gmail.com", "password": "talha123", "username": "Talha"}
my_user_obj = User(email="talha@gmail.com", password="talha123", username="Talha")

loaded = user_schema.load(my_user_dict)
print(type(loaded))

unloaded1 = user_schema.dump(loaded)
print(unloaded1)
print(type(unloaded1))

unloaded2 = user_schema.dump(my_user_obj)
print(unloaded2)
print(type(unloaded2))
"""


@users.route("/register", methods=["POST"])
@use_args(
    {
        "username": fields.Str(required=True, validate=validate.Length(max=20)),
        "email": fields.Email(required=True, validate=validate.Length(max=120)),
        "password": fields.Str(required=True, validate=validate.Length(max=60)),
    }
)
def register(args):
    try:
        # Marshmallow - Validate
        user = user_schema.load(request.json)

        # Give error if user already exist
        if user_exists(user.email):
            return jsonify({"error": "User with this email already exists"}), 422
        # Otherwise add user to database
        else:
            new_user = user_schema.dump(user)
            db.session.add(user)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "User successfully created",
                        "user": new_user,
                    }
                ),
                202,
            )

    # return validation error
    except ValidationError as err:
        return jsonify({"error": err.messages}), 500


@users.route("/login", methods=["POST"])
@use_args(
    {
        "email": fields.Email(required=True, validate=validate.Length(max=120)),
        "password": fields.Str(required=True, validate=validate.Length(max=60)),
    }
)
def login(args):
    # Get User by Email
    user = User.query.filter_by(email=args["email"]).first()

    # If User does not exist
    if not user:
        return jsonify({"error": "Email does not exist"}), 422
    # If Password entered is correct
    if user.password == args["password"]:
        session["user"] = user
        session["email"] = args["email"]
        return jsonify({"message": "Login Successful"}), 200
    # If Invalid password
    else:
        return jsonify({"error": "Invalid Password"}), 422


@users.route("/logout")
def logout():
    # Return error if User does not exist in session
    if not session["user"]:
        return jsonify({"error": "No one is logged in right now"})
    # Logout if User exist in session
    else:
        session["user"] = None
        return jsonify({"message": "User logged out successfuly"})


@users.route("/account")
def account():
    # Return User if exist in session
    if session.get("user"):
        return jsonify({"user": {"email": session["email"]}})
    # Return error if no account logged in
    else:
        return jsonify({"message": "No one logged in right now"})
