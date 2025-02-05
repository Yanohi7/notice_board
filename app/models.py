from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# створюється модель користувача для бази даних
class User(db.Model):
    """Модель користувача (студента або викладача)"""
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор користувача
    email = db.Column(db.String(150), unique=True, nullable=False)  # Унікальний email
    password_hash = db.Column(db.String(256), nullable=False)  # Хешований пароль
    role = db.Column(db.String(10), nullable=False)  # Роль користувача: 'student' або 'teacher'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата створення користувача

    def set_password(self, password):
        """Метод для хешування пароля перед збереженням у базі"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Метод для перевірки введеного пароля з хешованим паролем у базі"""
        return check_password_hash(self.password_hash, password)


class Announcement(db.Model):
    """модель оголошення, яке створює викладач"""
    id = db.Column(db.Integer, primary_key=True)  # унікальний ідентифікатор оголошення
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # ID викладача, який створив оголошення
    title = db.Column(db.String(255), nullable=False)  # заголовок оголошення
    message = db.Column(db.Text, nullable=False)  # текст повідомлення
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # дата створення оголошення


class AnnouncementReceiver(db.Model):
    """модель для збереження студентів, які отримали оголошення"""
    id = db.Column(db.Integer, primary_key=True)  # унікальний ідентифікатор запису
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcement.id"), nullable=False)  # ID оголошення
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # ID студента, який отримав повідомлення
    email_sent = db.Column(db.Boolean, default=False)  # чи було відправлено email студенту (True/False)
