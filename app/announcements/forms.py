from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class CreateAnnouncementForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    body = TextAreaField("Текст оголошення", validators=[DataRequired()])

    faculty = SelectField("Факультет", coerce=int, choices=[])
    department = SelectField("Кафедра", coerce=int, choices=[])
    group = SelectField("Група", coerce=int, choices=[])
    subject = SelectField("Предмет", coerce=int, choices=[])

    search = StringField("Пошук студента")

    # Додано поле для вибору отримувачів
    receivers = SelectMultipleField("Одержувачі", coerce=int, choices=[])

    submit = SubmitField("Надіслати")

    
class EditAnnouncementForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=255)])
    body = TextAreaField("Текст оголошення", validators=[DataRequired()])
    submit = SubmitField("Зберегти зміни")