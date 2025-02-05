from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Announcement, AnnouncementReceiver, User
from app.announcements import announcements_bp
from app.announcements.forms import AnnouncementForm

@announcements_bp.route("/")
@login_required
def list_announcements():
    """Список оголошень"""
    if current_user.role == "teacher":
        announcements = Announcement.query.filter_by(teacher_id=current_user.id).all()
    else:
        announcements = (
            db.session.query(Announcement)
            .join(AnnouncementReceiver)
            .filter(AnnouncementReceiver.student_id == current_user.id)
            .all()
        )
    return render_template("announcements/list.html", announcements=announcements)
@announcements_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_announcement():
    """Створення нового оголошення (тільки для викладачів)"""
    if current_user.role != "user": # ПОКИ ЩО БЕЗ РОЛІ ВИКЛАДАЧА!!!
        flash("У вас немає прав для створення оголошень", "danger")
        return redirect(url_for("announcements.list_announcements"))

    form = AnnouncementForm()
    form.students.choices = [(s.id, s.email) for s in User.query.filter_by(role="user").all()] # ПОКИ ЩО РОЛЬ ЮЗЕРА, А НЕ СТУДЕНТА

    if form.validate_on_submit():
        new_announcement = Announcement(
            teacher_id=current_user.id, title=form.title.data, message=form.message.data
        )
        db.session.add(new_announcement)
        db.session.commit()

        for student_id in form.students.data:
            receiver = AnnouncementReceiver(
                announcement_id=new_announcement.id, student_id=student_id
            )
            db.session.add(receiver)

        db.session.commit()

        flash("Оголошення успішно створено!", "success")
        return redirect(url_for("announcements.list_announcements"))

    return render_template("announcements/create.html", form=form)
