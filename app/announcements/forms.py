from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
    
class CreateAnnouncementForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    body = TextAreaField("Текст оголошення", validators=[DataRequired()])
    category = SelectField("Категорія", coerce=int, choices=[])
    faculty = SelectField("Факультет", coerce=int, choices=[], validate_choice=False)
    department = SelectField("Кафедра", coerce=int, choices=[], validate_choice=False)
    group = SelectField("Група", coerce=int, choices=[], validate_choice=False)
    subject = SelectField("Предмет", coerce=int, choices=[], validate_choice=False)

    search = StringField("Пошук студента")
    receivers = SelectMultipleField("Одержувачі", coerce=int, choices=[])

    submit = SubmitField("Надіслати")

class EditAnnouncementForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    body = TextAreaField("Текст оголошення", validators=[DataRequired()])

    category = SelectField("Категорія", coerce=int, choices=[])
    receivers = SelectMultipleField("Отримувачі", coerce=int, choices=[])

    submit = SubmitField("Оновити")
