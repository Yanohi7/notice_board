from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Announcement, AnnouncementRecipient, User
from app.announcements import announcements_bp
from app.announcements.forms import AnnouncementForm

@announcements_bp.route("/")
@login_required
def list_announcements():
    """Список активних оголошень"""
    if current_user.role == "teacher":
        announcements = Announcement.query.filter_by(teacher_id=current_user.id, archived=False).all()
    else:
        announcements = (
            db.session.query(Announcement)
            .join(AnnouncementRecipient)
            .filter(AnnouncementRecipient.student_id == current_user.id, Announcement.archived == False)
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
            receiver = AnnouncementRecipient(
                announcement_id=new_announcement.id, student_id=student_id
            )
            db.session.add(receiver)

        db.session.commit()

        flash("Оголошення успішно створено!", "success")
        return redirect(url_for("announcements.list_announcements"))

    return render_template("announcements/create.html", form=form)


@announcements_bp.route("/archive/<int:announcement_id>", methods=["POST"])
@login_required
def archive_announcement(announcement_id):
    """Архівування оголошення"""
    announcement = Announcement.query.get_or_404(announcement_id)

    if current_user.id != announcement.teacher_id:
        flash("Ви не можете архівувати це оголошення", "danger")
        return redirect(url_for("announcements.list_announcements"))

    announcement.archived = True
    db.session.commit()
    flash("Оголошення архівоване", "success")
    return redirect(url_for("announcements.list_announcements"))

@announcements_bp.route("/archived")
@login_required
def list_archived_announcements():
    """Список архівованих оголошень"""
    if current_user.role == "teacher":
        announcements = Announcement.query.filter_by(teacher_id=current_user.id, archived=True).all()
    else:
        announcements = (
            db.session.query(Announcement)
            .join(AnnouncementRecipient)
            .filter(AnnouncementRecipient.student_id == current_user.id, Announcement.archived == True)
            .all()
        )
    return render_template("announcements/archived.html", announcements=announcements)
