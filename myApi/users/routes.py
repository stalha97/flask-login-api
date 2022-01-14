from flask import request, Blueprint, session, jsonify
from marshmallow.exceptions import ValidationError
from myApi import db
from myApi.models import User
from myApi.users.schemas import UserSchema
from myApi.users.utils import user_exists


users = Blueprint("users", __name__)

user_schema = UserSchema()


# @users.route("/register", methods=["POST"])
# def register():
#     errors = user_schema.validate(request.json)
#     if errors:
#         return {
#             "errors": errors,
#         }, 500
#     else:
#         user = user_schema.load(request.json)
#         print(user)
#         # print(user.email)
#         if user_exists(user.email):
#             return {"error": "User with this email already exists"}, 422

#         db.session.add(user)
#         db.session.commit()

#         return {"message": "User successfully created"}, 202


@users.route("/register", methods=["POST"])
def register():
    try:
        # Marshmallow - Validate
        user = user_schema.load(request.json)
        print(dir(request))
        print(user)

        # Give error if user already exist
        if user_exists(user.email):
            return {"error": "User with this email already exists"}, 422
        # Otherwise add user to database
        else:
            db.session.add(user)
            db.session.commit()
            return {"message": "User successfully created"}, 202

    # return validation error
    except ValidationError as err:
        return {"errors": err.messages}, 500


@users.route("/login", methods=["POST"])
def login():
    req = request.json
    if not req.get("email") or not req.get("password"):
        return {"error": "Email or Password missing"}

    errors = user_schema.validate(
        {"email": req["email"], "password": req["password"]}, partial=True
    )
    if errors:
        return {
            "errors": errors,
        }, 500
    else:
        user = User.query.filter_by(email=req["email"]).first()
        if not user:
            return {"error": "Email does not exist"}
        if user.password == req["password"]:
            session["user"] = user
            session["email"] = req["email"]
            return {"message": "Login Successful"}, 200
        else:
            return {"error": "Invalid Password"}


@users.route("/logout")
def logout():
    if not session["user"]:
        return {"error": "No one is logged in right now"}
    else:
        session["user"] = None
        return {"message": "User logged out successfuly"}


@users.route("/account")
def account():
    if session.get("user"):
        return {"user": {"email": session["email"]}}
    else:
        return {"message": "No one logged in right now"}
