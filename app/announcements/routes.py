from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Announcement, AnnouncementRecipient, User
from app.announcements import announcements_bp
from app.announcements.forms import CreateAnnouncementForm, EditAnnouncementForm

@announcements_bp.route("/", methods=["GET"])
@login_required
def list_announcements():
    announcements = db.session.query(Announcement).join(AnnouncementRecipient).filter(
        AnnouncementRecipient.user_id == current_user.id
    ).order_by(Announcement.created_at.desc()).all()

    return render_template("announcements/list.html", announcements=announcements)


@announcements_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_announcement():
    form = CreateAnnouncementForm()

    if form.validate_on_submit():
        student = User.query.filter_by(email=form.student_email.data).first()

        if not student:
            flash("Студента з таким email не знайдено!", "danger")
            return render_template("create_announcement.html", title="Створення оголошення", form=form)

        announcement = Announcement(
            title=form.title.data,
            body=form.body.data,
            author_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()

        # Додаємо студента в отримувачі оголошення
        announcement_recipient = AnnouncementRecipient(
            announcement_id=announcement.id,
            user_id=student.id  # Замість student_id
        )

        db.session.add(announcement_recipient)
        db.session.commit()

        flash("Оголошення опубліковано!", "success")
        return redirect(url_for("announcements.list_announcements"))

    return render_template("announcements/create.html", title="Створення оголошення", form=form)


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
    
    return render_template("announcements/edit.html", title="Редагування оголошення", form=form, announcement=announcement)

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


@announcements_bp.route("/sent", methods=["GET"])
@login_required
def sent_announcements():
    sent_announcements = Announcement.query.filter_by(author_id=current_user.id).order_by(
        Announcement.created_at.desc()).all()

    return render_template("announcements/sent.html", title="Надіслані оголошення",
                           sent_announcements=sent_announcements)


