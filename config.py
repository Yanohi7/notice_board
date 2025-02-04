import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")  # ключ з .flaskenv або резервне значення
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
