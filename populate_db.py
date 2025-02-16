from app import app, db
from app.models import User, UserRole, Faculty, Department, Group, Subject, AnnouncementCategory
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_users():
    """Створює тестових користувачів та заповнює базу."""
    with app.app_context():
        try:
            # Очищуємо базу
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

        # Створюємо факультети
        faculty1 = Faculty(name="Факультет комп'ютерних наук")
        faculty2 = Faculty(name="Факультет економіки")

        db.session.add_all([faculty1, faculty2])
        db.session.commit()

        # Створюємо кафедри
        department1 = Department(name="Кафедра програмної інженерії", faculty_id=faculty1.id)
        department2 = Department(name="Кафедра економіки", faculty_id=faculty2.id)

        db.session.add_all([department1, department2])
        db.session.commit()

        # Створюємо групи
        group1 = Group(name="КН-41", department_id=department1.id)
        group2 = Group(name="КН-42", department_id=department1.id)
        group3 = Group(name="ЕК-21", department_id=department2.id)
        group4 = Group(name="ЕК-22", department_id=department2.id)

        db.session.add_all([group1, group2, group3, group4])
        db.session.commit()

        # Функція для створення користувачів
        def create_user(username, email, password, role, faculty=None, department=None, group=None):
            user = User(
                username=username,
                email=email,
                role=role,
                faculty_id=faculty.id if faculty else None,
                department_id=department.id if department else None,
                group_id=group.id if group else None,
            )
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')  # Хешуємо пароль
            db.session.add(user)

        # Створюємо викладачів
        teacher1 = User(
            username="teacher1",
            email="teacher1@example.com",
            role=UserRole.TEACHER,
            faculty_id=faculty1.id,
            department_id=department1.id,
        )
        teacher1.password = bcrypt.generate_password_hash("teacher123").decode('utf-8')

        teacher2 = User(
            username="teacher2",
            email="teacher2@example.com",
            role=UserRole.TEACHER,
            faculty_id=faculty2.id,
            department_id=department2.id,
        )
        teacher2.password = bcrypt.generate_password_hash("teacher123").decode('utf-8')

        db.session.add_all([teacher1, teacher2])
        db.session.commit()

        # Створюємо предмети
        subject1 = Subject(name="Алгоритми та структури даних", department_id=department1.id, teacher_id=teacher1.id)
        subject2 = Subject(name="Економіка підприємства", department_id=department2.id, teacher_id=teacher2.id)

        db.session.add_all([subject1, subject2])
        db.session.commit()

        # Створюємо студентів
        students = [
            ("student1", "student1@example.com", "student123", faculty1, department1, group1),
            ("student2", "student2@example.com", "student123", faculty1, department1, group1),
            ("student3", "student3@example.com", "student123", faculty1, department1, group2),
            ("student4", "student4@example.com", "student123", faculty2, department2, group3),
            ("student5", "student5@example.com", "student123", faculty2, department2, group4),
        ]

        for username, email, password, faculty, department, group in students:
            create_user(username, email, password, UserRole.STUDENT, faculty, department, group)

        db.session.commit()

        # Додаємо категорії оголошень
        categories = [
            AnnouncementCategory(name="Навчання"),
            AnnouncementCategory(name="Олімпіади"),
            AnnouncementCategory(name="Загальні повідомлення"),
            AnnouncementCategory(name="Наукові дослідження"),
        ]

        db.session.add_all(categories)
        db.session.commit()

        print("✅ База даних успішно заповнена!")

# Виконати скрипт
if __name__ == "__main__":
    create_users()
