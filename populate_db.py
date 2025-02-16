from app import app, db  # Імпортуємо app через create_app (якщо є) або напряму
from app.models import User, UserRole, Faculty, Department, Group, Subject, AnnouncementCategory
from werkzeug.security import generate_password_hash

# Створюємо додаток та відкриваємо контекст

with app.app_context():  # Відкриваємо контекст додатку
    try:
        db.session.rollback()
        db.session.query(AnnouncementCategory).delete()
        db.session.query(Subject).delete()
        db.session.query(Group).delete()
        db.session.query(Department).delete()
        db.session.query(Faculty).delete()
        db.session.query(User).delete()
        db.session.commit()
    except Exception as e:
        print(f"Помилка при очищенні бази: {e}")
        db.session.rollback()

    # Створення факультетів
    faculty1 = Faculty(name="Факультет комп'ютерних наук")
    faculty2 = Faculty(name="Факультет економіки")

    db.session.add_all([faculty1, faculty2])
    db.session.commit()

    # Створення кафедр
    department1 = Department(name="Кафедра програмної інженерії", faculty_id=faculty1.id)
    department2 = Department(name="Кафедра економіки", faculty_id=faculty2.id)

    db.session.add_all([department1, department2])
    db.session.commit()

    # Створення груп
    group1 = Group(name="КН-41", department_id=department1.id)
    group2 = Group(name="КН-42", department_id=department1.id)
    group3 = Group(name="ЕК-21", department_id=department2.id)
    group4 = Group(name="ЕК-22", department_id=department2.id)

    db.session.add_all([group1, group2, group3, group4])
    db.session.commit()

    # Створення викладачів
    teacher1 = User(
        username="teacher1",
        email="teacher1@example.com",
        password=generate_password_hash("teacher123"),
        role=UserRole.TEACHER,
        faculty_id=faculty1.id,
        department_id=department1.id,
    )

    teacher2 = User(
        username="teacher2",
        email="teacher2@example.com",
        password=generate_password_hash("teacher123"),
        role=UserRole.TEACHER,
        faculty_id=faculty2.id,
        department_id=department2.id,
    )

    db.session.add_all([teacher1, teacher2])
    db.session.commit()

    # Створення предметів
    subject1 = Subject(name="Алгоритми та структури даних", department_id=department1.id, teacher_id=teacher1.id)
    subject2 = Subject(name="Економіка підприємства", department_id=department2.id, teacher_id=teacher2.id)

    db.session.add_all([subject1, subject2])
    db.session.commit()

    # Створення студентів і прив’язка до груп
    students = [
        User(username="student1", email="student1@example.com", password=generate_password_hash("student123"), role=UserRole.STUDENT, faculty_id=faculty1.id, department_id=department1.id, group_id=group1.id),
        User(username="student2", email="student2@example.com", password=generate_password_hash("student123"), role=UserRole.STUDENT, faculty_id=faculty1.id, department_id=department1.id, group_id=group1.id),
        User(username="student3", email="student3@example.com", password=generate_password_hash("student123"), role=UserRole.STUDENT, faculty_id=faculty1.id, department_id=department1.id, group_id=group2.id),
        User(username="student4", email="student4@example.com", password=generate_password_hash("student123"), role=UserRole.STUDENT, faculty_id=faculty2.id, department_id=department2.id, group_id=group3.id),
        User(username="student5", email="student5@example.com", password=generate_password_hash("student123"), role=UserRole.STUDENT, faculty_id=faculty2.id, department_id=department2.id, group_id=group4.id),
    ]

    db.session.add_all(students)
    db.session.commit()

    # Додавання категорій оголошень
    categories = [
        AnnouncementCategory(name="Навчання"),
        AnnouncementCategory(name="Олімпіади"),
        AnnouncementCategory(name="Загальні повідомлення"),
        AnnouncementCategory(name="Наукові дослідження"),
    ]

    db.session.add_all(categories)
    db.session.commit()

    print("✅ База даних успішно заповнена!")
