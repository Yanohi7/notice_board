from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app import User

# створюється форма входу
class LoginForm(FlaskForm):
    # поле для введення email з валідацією
    email = StringField('Email', validators=[DataRequired(), Email()])
    # поле для введення пароля з мінімальною довжиною 6 символів
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    # кнопка для відправлення форми
    submit = SubmitField('Увійти')

# створюється форма реєстрації
class RegisterForm(FlaskForm):
    # поле для введення email з валідацією
    email = StringField('Email', validators=[DataRequired(), Email()])
    # поле для введення пароля з мінімальною довжиною 6 символів
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    # поле для підтвердження пароля, яке має збігатися з основним паролем
    confirm_password = PasswordField('Підтвердження паролю',
                                     validators=[DataRequired(), EqualTo('password')])
    # кнопка для відправлення форми
    submit = SubmitField('Зареєструватися')

    # перевіряється, чи вже існує користувач з таким email у базі даних
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже використовується.')
