from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from app import oauth

# маршрут для головної сторінки
@app.route("/")
def home():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# маршрут для реєстрації нового користувача
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # створюється новий користувач і хешується його пароль
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        # додається користувач у базу даних
        db.session.add(user)
        db.session.commit()
        # автоматичний вхід після реєстрації
        login_user(user)
        flash("Реєстрація успішна!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

# маршрут для входу користувача
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # шукається користувач за email
        user = User.query.filter_by(email=form.email.data).first()
        # перевіряється правильність пароля
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вхід успішний!", "success")
            return redirect(url_for("home"))
        else:
            flash("Невірний email або пароль", "danger")
    return render_template("login.html", form=form)

# маршрут для виходу користувача з системи
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунту", "info")
    return redirect(url_for("home"))

@app.route("/google-login")
def googleLogin():
    return oauth.NoticeBoard.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))


@app.route("/signin-google")
def googleCallback():
    token = oauth.NoticeBoard.authorize_access_token()
    user_info = token.get("userinfo")  # Отримуємо дані користувача

    if not user_info:
        return redirect(url_for("login"))  # Якщо немає даних – повертаємо на сторінку входу

    email = user_info.get("email")
    if not email:
        return redirect(url_for("login"))  # Якщо немає email – не можемо автентифікувати

    user = User.query.filter_by(email=email).first()

    if not user:
        # Якщо користувача немає, створюємо нового
        user = User(email=email, name=user_info.get("name"))
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)  # Логуємо користувача через Flask-Login

    return redirect(url_for("home"))
