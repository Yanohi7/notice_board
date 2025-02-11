from app import app, db
from app.models import User

with app.app_context():
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            password=User.hash_password("StrongPass123"),
            role=0
        )
        db.session.add(admin)
        db.session.commit()
        print("Адміністратор створений успішно!")
    else:
        print("Адміністратор вже існує.")
