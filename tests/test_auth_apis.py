import unittest
from myApi import create_app

# from flask_sqlalchemy import SQLAlchemy
from myApi.models import *
import json

# db = SQLAlchemy()
# test_app = create_app()
# test_app.testing = True
# test_app.debug = False
# client = test_app.test_client()

# ctx = test_app.test_request_context()
# ctx.push()
# test_app.preprocess_request()

# test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
# test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(test_app)
# # db.init_app(test_app)
# db.create_all()
# User.query.all()


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.const_user = {
            "username": "TalhaTest",
            "email": "talhaTest@gmail.com",
            "password": "talha123",
        }
        self.test_app = create_app()
        self.test_app.testing = True
        self.test_app.debug = False
        self.client = self.test_app.test_client()

        self.ctx = self.test_app.test_request_context()
        self.test_app.test_request_context().push()
        self.test_app.preprocess_request()

        # In-Memory Database
        self.test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.test_app)
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_correct(self):
        user = self.const_user.copy()
        res = self.client.post("/register", json=user)
        # print(res.data)
        self.assertEqual(res.status_code, 202)

    # register user with missing fields
    # def test_register_user_missing_fields(self):
    #     const_user = self.const_user

    #     user = const_user.copy()
    #     del user["username"]
    #     res = client.post("/register", data=user, content_type="application/json")
    #     self.assertEqual(res.status_code, 422)

    #     user = const_user.copy()
    #     del user["email"]
    #     res = client.post("/register", data=user, content_type="application/json")
    #     self.assertEqual(res.status_code, 422)

    #     user = const_user.copy()
    #     del user["password"]
    #     res = client.post("/register", data=user, content_type="application/json")
    #     self.assertEqual(res.status_code, 422)

    # register user with invalid values
    # def test_register_user_invalid_values(self):
    #     const_user = self.const_user
    #     # print(const_user)

    #     user = const_user.copy()
    #     user["username"] = "a" * 30
    #     res = self.client.post("/register", data=json.dumps(user))
    #     breakpoint()
    #     self.assertEqual(res.status_code, 422)

    #     user = const_user.copy()
    #     user["email"] = "wrong_email_format"
    #     res = client.post("/register", data=json.dumps(user))
    #     self.assertEqual(res.status_code, 422)

    #     user = const_user.copy()
    #     user["password"] = "a" * 65

    #     print(user)
    #     res = client.post("/register", data=json.dumps(user))
    #     print(res.data)
    #     self.assertEqual(res.status_code, 422)

    # register user, pass extra values in request

    # login user with missing fields
    # login user with invalid values
    # login user, pass extra values in request
    # login user, while user is already logged in

    # logout user when user is logged in
    # logout user when no user is logged in

    # fetch account when user is logged in
    # fetch account when user is not logged in


if __name__ == "__main__":
    unittest.main()
