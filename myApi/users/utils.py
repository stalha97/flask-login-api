# from myApi import db
from myApi.models import User


def user_exists(email):
    # return User.query.filter(User.email == email).first() is not None

    user = User.query.filter(User.email == email).first()
    if user:
        return True
    else:
        return False
