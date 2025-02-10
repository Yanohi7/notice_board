from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# створюється екземпляр додатку flask
app = Flask(__name__)
# завантажується конфігурація з файлу config.py
app.config.from_object(Config)

# ініціалізується база даних sqlalchemy
db = SQLAlchemy(app)
# ініціалізується flask-migrate для керування міграціями бази даних
migrate = Migrate(app, db)
# ініціалізується bcrypt для хешування паролів
bcrypt = Bcrypt(app)
# ініціалізується login manager для керування аутентифікацією користувачів
login_manager = LoginManager(app)
# задається маршрут для перенаправлення неавторизованих користувачів
login_manager.login_view = "login"

# імпортується модель користувача, щоб працювати з нею у додатку
from app.models import User, Announcement, AnnouncementRecipient

# задається функція завантаження користувача flask-login за його id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.announcements import announcements_bp
app.register_blueprint(announcements_bp, url_prefix="/announcements") # реєстрація блюпринта


# імпортуються маршрути додатку
from app import routes
