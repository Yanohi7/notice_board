from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Announcement, AnnouncementRecipient, User
from app.announcements import announcements_bp
from app.announcements.forms import CreateAnnouncementForm, EditAnnouncementForm

@announcements_bp.route("/", methods=["GET"])
@login_required
def list_announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("announcements_list.html", title="Оголошення", announcements=announcements)

@announcements_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_announcement():
    form = CreateAnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            body=form.body.data,
            author_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash("Оголошення опубліковано!", "success")
        return redirect(url_for("announcements.list_announcements"))
    
    return render_template("create_announcement.html", title="Створення оголошення", form=form)

@announcements_bp.route("/edit/<int:announcement_id>", methods=["GET", "POST"])
@login_required
def edit_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    
    if announcement.author_id != current_user.id and current_user.role != 0:
        flash("Ви не маєте прав редагувати це оголошення!", "danger")
        return redirect(url_for("announcements.list_announcements"))

    form = EditAnnouncementForm(obj=announcement)
    
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.body = form.body.data
        db.session.commit()
        flash("Оголошення оновлено!", "success")
        return redirect(url_for("announcements.list_announcements"))
    
    return render_template("edit_announcement.html", title="Редагування оголошення", form=form, announcement=announcement)

@announcements_bp.route("/delete/<int:announcement_id>", methods=["POST"])
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)

    if announcement.author_id != current_user.id and current_user.role != 0:
        flash("Ви не маєте прав видалити це оголошення!", "danger")
        return redirect(url_for("announcements.list_announcements"))

    db.session.delete(announcement)
    db.session.commit()
    flash("Оголошення видалено!", "success")
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
