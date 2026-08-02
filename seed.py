from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole

def seed_data():
    db = SessionLocal()
    try:
        # Check if PM exists
        pm = db.query(User).filter(User.email == "pm@example.com").first()
        if not pm:
            pm = User(
                email="pm@example.com",
                name="Project Manager",
                password_hash=get_password_hash("password123"),
                role=UserRole.PM_IT
            )
            db.add(pm)
            
        # Check if Staff exists
        staff = db.query(User).filter(User.email == "staff@example.com").first()
        if not staff:
            staff = User(
                email="staff@example.com",
                name="Staff IT",
                password_hash=get_password_hash("password123"),
                role=UserRole.STAFF_IT
            )
            db.add(staff)

        # Check if User exists
        user = db.query(User).filter(User.email == "user@example.com").first()
        if not user:
            user = User(
                email="user@example.com",
                name="Regular User",
                password_hash=get_password_hash("password123"),
                role=UserRole.USER
            )
            db.add(user)
            
        db.commit()
        print("Seed data completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
