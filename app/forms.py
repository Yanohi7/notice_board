from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

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
    username = StringField("Ім'я користувача", validators=[DataRequired()])
    # поле для введення email з валідацією
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # поле для введення пароля з вимогами до складності
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(),
            Length(min=6, message='Пароль має містити щонайменше 6 символів'),
            Regexp(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$",
            message="Пароль має містити принаймні одну малу, одну велику літеру та одну цифру"
            )
        ]
    )
    
    # поле для підтвердження пароля, яке має збігатися з основним паролем
    confirm_password = PasswordField(
        'Підтвердження паролю',
        validators=[DataRequired(), EqualTo('password', message='Паролі мають збігатися')]
    )
    
    # кнопка для відправлення форми
    submit = SubmitField('Зареєструватися')

    # перевіряється, чи вже існує користувач з таким email у базі даних
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже використовується.')
