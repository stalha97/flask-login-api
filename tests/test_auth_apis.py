import unittest
from myApi import create_app

# from flask_sqlalchemy import SQLAlchemy
from myApi.models import *

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
        self.test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.test_app)
        db.create_all()

    def tearDown(self):
        db.drop_all()

    # Register Happy/Correct Case
    def test_register_correct_case(self):
        user = self.const_user.copy()
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 202)
        return user

    # register user with missing fields
    def test_register_user_missing_fields(self):
        const_user = self.const_user

        # Test Missing Username
        user = const_user.copy()
        del user["username"]
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Test Missing Email
        user = const_user.copy()
        del user["email"]
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Test Missing Password
        user = const_user.copy()
        del user["password"]
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # register user with invalid values
    def test_register_user_invalid_values(self):
        const_user = self.const_user

        # Test Invalid Username
        user = const_user.copy()
        user["username"] = "a" * 30
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Test Invalid Email
        user = const_user.copy()
        user["email"] = "wrong_email_format"
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Test Invalid Password
        user = const_user.copy()
        user["password"] = "a" * 65
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # register user, pass extra values in request
    def test_register_extra_values_in_request(self):
        const_user = self.const_user

        # Test Invalid Username
        user = const_user.copy()
        user["an_extra_field"] = "extra field"
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # register when an account already exists
    def test_register_user_already_exists(self):
        const_user = self.const_user.copy()

        user = const_user.copy()
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 202)

        user = const_user.copy()
        user["username"] = "User2 repeated"
        res = self.client.post("/register", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # login happy case
    def test_login_happy_case(self):
        user = self.test_register_correct_case()
        del user["username"]
        res = self.client.post("/login", json=user)
        self.assertEqual(res.status_code, 200)

        return user

    # login user with missing fields
    def test_login_user_missing_fields(self):
        const_user = self.test_register_correct_case()
        del const_user["username"]

        # Missing field # 1 (email)
        user = const_user.copy()
        del user["email"]
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Missing field # 2 (password)
        user = const_user.copy()
        del user["password"]
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # login user with invalid values
    def test_login_user_invalid_values(self):
        const_user = self.test_register_correct_case()
        del const_user["username"]

        # Missing field # 1 (email)
        user = const_user.copy()
        user["email"] = "non-valid-email"
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Missing field # 2 (password)
        user = const_user.copy()
        user["password"] = "a" * 70
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # login user with invalid value types
    def test_login_user_invalid_value_types(self):
        const_user = self.test_register_correct_case()
        del const_user["username"]

        # Invalid value for # 1 (email)
        user = const_user.copy()
        user["email"] = 55
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

        # Invalid value for # 2 (password)
        user = const_user.copy()
        user["password"] = 55
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # login user, pass extra values in request
    def test_login_user_extra_values_in_request(self):
        const_user = self.test_register_correct_case()
        del const_user["username"]

        # Extra values in request
        user = const_user.copy()
        user["extra_field"] = 55
        res = self.client.post("/login", json=user)
        # print(res.json)
        self.assertEqual(res.status_code, 422)

    # login user, while user is already logged in
    # def test_login_when_already_loggedin(self):
    #     logged_in_user = self.test_login_happy_case()

    #     res = self.client.post("/login", json=logged_in_user)
    #     print(res.json)
    #     self.assertEqual(res.status_code, 422)

    # logout user when user is logged in
    # logout user when no user is logged in

    # fetch account when user is logged in
    # fetch account when user is not logged in


if __name__ == "__main__":
    unittest.main()
