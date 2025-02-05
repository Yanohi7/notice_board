from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# створюється модель користувача для бази даних
class User(db.Model, UserMixin):
    """модель користувача"""
    id = db.Column(db.Integer, primary_key=True)  # унікальний ідентифікатор користувача
    email = db.Column(db.String(150), unique=True, nullable=False)  # унікальний email
    password_hash = db.Column(db.String(256), nullable=False)  # хешований пароль
    role = db.Column(db.String(10), default="user", nullable=False)  # роль за замовчуванням "user"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # дата створення користувача

    def set_password(self, password):
        """метод для хешування пароля перед збереженням у базі"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """метод для перевірки введеного пароля з хешованим паролем"""
        return check_password_hash(self.password_hash, password)


class Announcement(db.Model):
    """Модель оголошення, яке створює викладач"""
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived = db.Column(db.Boolean, default=False)  # НОВЕ поле для архівування


class AnnouncementReceiver(db.Model):
    """модель для збереження студентів, які отримали оголошення"""
    id = db.Column(db.Integer, primary_key=True)  # унікальний ідентифікатор запису
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcement.id"), nullable=False)  # ID оголошення
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # ID студента, який отримав повідомлення
    email_sent = db.Column(db.Boolean, default=False)  # чи було відправлено email студенту (True/False)