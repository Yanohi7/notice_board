
from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, logout_user, login_required

@app.route("/")
def home():
    return render_template("index.html", title="Notice Board")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)  # ✅ Використовуємо метод User
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Реєстрація успішна!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Реєстрація", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # ✅ Перевіряємо пароль
            login_user(user)
            flash("Вхід успішний!", "success")
            return redirect(url_for("home"))
        else:
            flash("Невірний email або пароль", "danger")
    return render_template("login.html", title="Вхід", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунту", "info")
    return redirect(url_for("home"))
