import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OUATH2_CLIENT_ID = os.getenv("OUATH2_CLIENT_ID")
    OUATH2_CLIENT_SECRET = os.getenv("OUATH2_CLIENT_SECRET")
    OUATH2_META_URL = os.getenv("OUATH2_META_URL")
