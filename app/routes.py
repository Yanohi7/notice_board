from flask import render_template, redirect, url_for, flash
from app import app, db, bcrypt
from app.forms import LoginForm, RegisterForm, EditUserForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from .utils import admin_required
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


# маршрут для редагування користувача
@app.route("/admin/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash("Користувача оновлено успішно!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("edit_user.html", title="Редагування користувача", form=form, user=user)

# маршрут для видалення користувача
@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Користувача видалено успішно!", "success")
    return redirect(url_for("admin_dashboard"))


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
    username = user_info.get("name")  # Отримуємо ім'я користувача

    if not email:
        return redirect(url_for("login"))  # Якщо немає email – не можемо автентифікувати

    user = User.query.filter_by(email=email).first()

    if not user:
        # Якщо користувача немає, створюємо нового
        user = User(
            email=email,
            username=username or "GoogleUser",  # Якщо ім'я не приходить, даємо дефолтне
            password=User.hash_password("defaultpassword"),  # Генеруємо тимчасовий пароль
            role=5  # 5 — студент за замовчуванням
        )
        db.session.add(user)
        db.session.commit()
    login_user(user, remember=True)  # Логуємо користувача через Flask-Login

    return redirect(url_for("home"))
