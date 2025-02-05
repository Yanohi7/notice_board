from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class AnnouncementForm(FlaskForm):
    """Форма для створення оголошення"""
    title = StringField("Заголовок", validators=[DataRequired()])
    message = TextAreaField("Повідомлення", validators=[DataRequired()])
    students = SelectMultipleField("Оберіть студентів", coerce=int)
    submit = SubmitField("Створити")
