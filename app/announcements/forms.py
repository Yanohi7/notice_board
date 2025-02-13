from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class CreateAnnouncementForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=255)])
    body = TextAreaField("Текст оголошення", validators=[DataRequired()])
    # Додаємо поле для вибору отримувачів
    receivers = SelectMultipleField("Одержувачі", coerce=int)
    submit = SubmitField("Опублікувати")
    
class EditAnnouncementForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=255)])
    body = TextAreaField("Текст оголошення", validators=[DataRequired()])
    submit = SubmitField("Зберегти зміни")