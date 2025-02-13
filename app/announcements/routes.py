from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Announcement, AnnouncementRecipient, User
from app.announcements import announcements_bp
from app.announcements.forms import CreateAnnouncementForm, EditAnnouncementForm
from flask_mail import Message
from app import mail


def send_email(recipient, subject, body, sender_email):
    msg = Message(subject, sender=sender_email, recipients=[recipient])
    msg.body = body
    mail.send(msg)

@announcements_bp.route("/", methods=["GET"])
@login_required
def list_announcements():
    announcements = (
        Announcement.query
        .join(AnnouncementRecipient)
        .filter(AnnouncementRecipient.user_id == current_user.id)
        .order_by(Announcement.created_at.desc())
        .all()
    )


    return render_template("announcements/list.html", announcements=announcements)



@announcements_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_announcement():
    if current_user.role not in [0, 1, 2, 3, 4]:  
        flash("Ви не маєте прав на створення оголошень!", "danger")
        return redirect(url_for("announcements.list_announcements"))

    form = CreateAnnouncementForm()
    form.receivers.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            body=form.body.data,
            author_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()

        sender_email = current_user.email  

        for user_id in form.receivers.data:
            recipient = AnnouncementRecipient(announcement_id=announcement.id, user_id=user_id)
            db.session.add(recipient)

            user = User.query.get(user_id)
            # if user:
            #     # send_email(
            #     #     user.email,
            #     #     f"Нове оголошення: {announcement.title}",
            #     #     f"{announcement.body}\n\nПереглянути: {url_for('announcements.announcement_detail', announcement_id=announcement.id, _external=True)}",
            #     #     sender_email
            #     # )

        db.session.commit()
        flash("Оголошення опубліковано та email-сповіщення надіслано!", "success")
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

    return render_template("announcements/edit.html", title="Редагування оголошення", form=form,
                           announcement=announcement)

@announcements_bp.route("/view/<int:announcement_id>", methods=["GET"])
@login_required
def announcement_detail(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    
    recipient = AnnouncementRecipient.query.filter_by(
        announcement_id=announcement_id, user_id=current_user.id
    ).first()
    
    if recipient and not recipient.is_read:
        recipient.is_read = True
        db.session.commit()
    
    return render_template("announcement_detail.html", title=announcement.title, announcement=announcement)

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
