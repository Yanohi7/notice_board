from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, bcrypt
from enum import IntEnum

class UserRole(IntEnum):
    ADMIN = 0
    RECTOR = 1
    DEAN_OFFICE = 2  # Об'єднана роль декана та працівників деканату
    HEAD_OF_DEPARTMENT = 3
    TEACHER = 4
    STUDENT = 5

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False)

    @staticmethod
    def hash_password(plain_password):
        return bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.password, plain_password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id', name='fk_department_faculty'), nullable=False)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', name='fk_subject_department'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_subject_teacher'), nullable=False)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', name='fk_group_department'), nullable=False)

class UserGroup(db.Model):
    __tablename__ = 'user_groups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_usergroup_user'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', name='fk_usergroup_group'), nullable=False)

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('announcement_categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref=db.backref('announcements', lazy=True))
    recipients = db.relationship('AnnouncementRecipient', back_populates='announcement', cascade="all, delete-orphan")



class AnnouncementRecipient(db.Model):
    __tablename__ = 'announcement_recipients'
    id = db.Column(db.Integer, primary_key=True)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcements.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    # Виправляємо: потрібно встановити `back_populates` на оголошення
    announcement = db.relationship('Announcement', back_populates='recipients')
    user = db.relationship('User', backref=db.backref('received_announcements', lazy=True))


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_file_user'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    permission_name = db.Column(db.String, nullable=False)


class AnnouncementCategory(db.Model):
    __tablename__ = 'announcement_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    announcements = db.relationship('Announcement', backref='category', lazy=True)

