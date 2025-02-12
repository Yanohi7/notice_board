from flask import Flask, session, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user
from config import Config
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# імпортується модель користувача, щоб працювати з нею у додатку
from app.models import User, Announcement, AnnouncementRecipient

oauth = OAuth(app)

oauth.register(
    "NoticeBoard",
    client_id=Config.OUATH2_CLIENT_ID,
    client_secret=Config.OUATH2_CLIENT_SECRET,
    server_metadata_url=Config.OUATH2_META_URL,
    client_kwargs={
        "scope": "openid profile email",
    }
)

# задається функція завантаження користувача flask-login за його id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



from app.announcements import announcements_bp
app.register_blueprint(announcements_bp, url_prefix="/announcements")
from app import routes
