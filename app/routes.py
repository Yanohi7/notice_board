from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from .utils import admin_required
# маршрут для головної сторінки
@app.route("/")
def home():
    return render_template("index.html", title="Notice Board")

# маршрут для реєстрації нового користувача
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Користувач з таким email вже існує!", "danger")
            return redirect(url_for("register"))

        user = User(
            username=form.username.data,  # Додано username
            email=form.email.data,
            password=User.hash_password(form.password.data),
            role=5  # За замовчуванням студент
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Реєстрація успішна!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="Реєстрація", form=form)


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
    
    return render_template("login.html", title="Вхід", form=form)

@app.route("/admin", methods=["GET"])
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template("admin_dashboard.html", title="Адмін-панель", users=users)


# маршрут для виходу користувача з системи
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунту", "info")
    return redirect(url_for("home"))
