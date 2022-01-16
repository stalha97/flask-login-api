# import os


class Config:
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = "7e6b2b777bc8a517033955216f5a4987e39940a26a8f2f4fe3ea6f409e225b25"
    SQLALCHEMY_DATABASE_URI = "sqlite:///mysite.db"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
