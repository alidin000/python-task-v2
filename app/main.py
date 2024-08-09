# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, schemas, crud, auth, database, moderation, deps
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

# Register new user
@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/", response_model=TokenResponse)
def login_for_access_token(login_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token, token_type="bearer")

# Create a post
@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

# Create a comment
@app.post("/posts/{post_id}/comments/", response_model=schemas.Comment)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(deps.get_current_user)):
    is_blocked = moderation.analyze_content(comment.content)
    return crud.create_comment(db=db, comment=comment, post_id=post_id, is_blocked=is_blocked)
