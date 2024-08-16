# app/crud.py
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.model_dump(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def create_comment(db: Session, comment: schemas.CommentCreate, post_id: int, is_blocked: bool):
    db_comment = models.Comment(**comment.model_dump(), post_id=post_id, is_blocked=is_blocked)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_analytics(db: Session, date_from: str, date_to: str):
    results = (
        db.query(
            func.date(models.Comment.created_at).label("date"),
            func.count(models.Comment.id).label("total_comments"),
            func.sum(models.Comment.is_blocked).label("blocked_comments"),
        )
        .filter(models.Comment.created_at >= date_from, models.Comment.created_at <= date_to)
        .group_by("date")
        .order_by("date")
        .all()
    )
    return results

def save_auto_response_settings(db: Session, post_id: int, settings: schemas.AutoResponseSettings):
    pass
