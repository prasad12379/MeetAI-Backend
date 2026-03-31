from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        return {
            "success": False,
            "message": "Email already exists",
            "user": None,
            "token": None
        }

    hashed_password = auth.hash_password(user.password)
    new_user = models.User(
        email=user.email,
        username=user.username,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = auth.create_token({"user_id": str(new_user.id)})

    return {
        "success": True,
        "message": "Account created successfully",
        "user": {
            "id": str(new_user.id),
            "email": new_user.email,
            "username": new_user.username
        },
        "token": token
    }

# Login
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not auth.verify_password(user.password, db_user.password):
        return {
            "success": False,
            "message": "Invalid email or password",
            "user": None,
            "token": None
        }

    token = auth.create_token({"user_id": str(db_user.id)})

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "id": str(db_user.id),
            "email": db_user.email,
            "username": db_user.username
        },
        "token": token
    }