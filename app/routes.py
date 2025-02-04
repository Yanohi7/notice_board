from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required

@app.route("/")
def home():
    return render_template("index.html", title="Notice Board")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
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
