import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OUATH2_CLIENT_ID = os.getenv("OUATH2_CLIENT_ID")
    OUATH2_CLIENT_SECRET = os.getenv("OUATH2_CLIENT_SECRET")
    OUATH2_META_URL = os.getenv("OUATH2_META_URL")


MAIL_SERVER = "smtp.mailtrap.io"
MAIL_PORT = 2525
MAIL_USERNAME = "4e06ece5c2626b"
MAIL_PASSWORD = "0bbf1499471189"
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = "noreply@university.com"
