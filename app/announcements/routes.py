from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from flask import jsonify
from app.models import Announcement, AnnouncementRecipient, User, UserRole, Group, Subject
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
    if current_user.role not in [UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN_OFFICE, UserRole.HEAD_OF_DEPARTMENT, UserRole.TEACHER]:  
        flash("Ви не маєте прав на створення оголошень!", "danger")
        return redirect(url_for("announcements.list_announcements"))

    form = CreateAnnouncementForm()

    # Динамічна генерація списку отримувачів залежно від ролі
    recipients_query = User.query

    if current_user.role == UserRole.TEACHER:
        # Викладач може надсилати оголошення лише студентам, які записані на його предмети
        recipients_query = recipients_query.join(Subject).filter(Subject.teacher_id == current_user.id)

    elif current_user.role == UserRole.HEAD_OF_DEPARTMENT:
        # Завідувач кафедри може надсилати оголошення всім студентам його кафедри
        recipients_query = recipients_query.filter(User.department_id == current_user.department_id)

    elif current_user.role == UserRole.DEAN_OFFICE:
        # Деканат може надсилати всім студентам факультету
        recipients_query = recipients_query.filter(User.faculty_id == current_user.faculty_id)

    elif current_user.role in [UserRole.RECTOR, UserRole.ADMIN]:
        # Ректор і адміністратор можуть надсилати всім користувачам
        pass  

    form.receivers.choices = [(user.id, user.username) for user in recipients_query.all()]

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

            # В майбутньому можна буде розкоментувати для надсилання email
            # user = User.query.get(user_id)
            # if user:
            #     send_email(
            #         user.email,
            #         f"Нове оголошення: {announcement.title}",
            #         f"{announcement.body}\n\nПереглянути: {url_for('announcements.announcement_detail', announcement_id=announcement.id, _external=True)}",
            #         sender_email
            #     )

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

@announcements_bp.route("/get_recipients", methods=["GET"])
@login_required
def get_recipients():
    faculty_id = request.args.get("faculty_id", type=int)
    department_id = request.args.get("department_id", type=int)
    group_id = request.args.get("group_id", type=int)
    subject_id = request.args.get("subject_id", type=int)
    search_query = request.args.get("search", type=str)

    query = User.query.filter(User.role == UserRole.STUDENT)  # Отримуємо студентів

    if faculty_id:
        query = query.filter(User.faculty_id == faculty_id)
    if department_id:
        query = query.filter(User.department_id == department_id)
    if group_id:
        query = query.join(Group).filter(Group.c.group_id == group_id)
    if subject_id:
        query = query.join(Subject).filter(Subject.subject_id == subject_id)
    if search_query:
        query = query.filter(User.username.ilike(f"%{search_query}%") | User.email.ilike(f"%{search_query}%"))

    recipients = [{"id": user.id, "name": user.username} for user in query.all()]
    return jsonify(recipients)

