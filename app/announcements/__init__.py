from flask import Blueprint

# створення блюпринта
announcements_bp = Blueprint('announcements', __name__,
                             template_folder='templates')

from app.announcements import routes  # імпортуємо маршрути
