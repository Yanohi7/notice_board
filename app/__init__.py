from flask import Flask, session, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user
from google.oauth2 import id_token
from google.auth.transport import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Імпортуємо моделі лише після ініціалізації db
from app.models import User  # 🔹 ВАЖЛИВО: імпортуємо тут!

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

GOOGLE_CLIENT_ID = "617019427896-8kpmb8bnfppdreolu6m0k7afggehcl96.apps.googleusercontent.com"

@app.route('/google-login', methods=['POST'])
def google_login():
    try:
        # Декодування JSON-запиту
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No JSON received"})

        token = data.get("token")

        if not token:
            return jsonify({"success": False, "error": "No token provided"})

        # Перевірка токена та продовження обробки
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        user_email = idinfo['email']
        user_name = idinfo.get('name', 'Користувач')

        user = User.query.filter_by(email=user_email).first()

        if not user:
            user = User(email=user_email, username=user_name, password_hash="google_oauth")
            db.session.add(user)
            db.session.commit()

        login_user(user)

        return jsonify({"success": True, "email": user_email})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})




from app.announcements import announcements_bp
app.register_blueprint(announcements_bp, url_prefix="/announcements")
from app import routes
