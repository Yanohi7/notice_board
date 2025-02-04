from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# створюється модель користувача для бази даних
class User(db.Model, UserMixin):
    # унікальний ідентифікатор користувача
    id = db.Column(db.Integer, primary_key=True)
    # email користувача, який має бути унікальним
    email = db.Column(db.String(120), unique=True, nullable=False)
    # хешований пароль користувача
    password_hash = db.Column(db.String(128), nullable=False)

    # метод для хешування пароля перед збереженням у базу даних
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # метод для перевірки правильності введеного пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
