# app/main.py
from typing import AsyncIterator
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, schemas, crud, auth, database, moderation, deps

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

async def database_lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Database initializing")
    database.init_db()
    yield
    print("Database shutdown")

app = FastAPI(lifespan=database_lifespan)

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
# login
@app.post("/login/", response_model=TokenResponse)
def login_for_access_token(login_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")

# Create a post
@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(deps.get_current_user)):
    print(f"Current user: {current_user.username} (ID: {current_user.id})")
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@app.post("/posts/{post_id}/comments/", response_model=schemas.Comment)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    is_blocked = moderation.analyze_content(comment.content)
    print(f"blocked: {is_blocked}")
    if is_blocked:
        raise HTTPException(status_code=400, detail="Comment contains inappropriate content and was blocked.")
    return crud.create_comment(db=db, comment=comment, post_id=post_id, is_blocked=is_blocked)


# Analytics on comments over a specified period
@app.get("/api/comments-daily-breakdown")
def comments_daily_breakdown(date_from: str, date_to: str, db: Session = Depends(database.get_db)):
    analytics = crud.get_comments_analytics(db=db, date_from=date_from, date_to=date_to)
    return analytics

# Automatic responses to comments
@app.post("/posts/{post_id}/auto-response/")
def set_auto_response(post_id: int, auto_response: schemas.AutoResponseSettings, db: Session = Depends(database.get_db), current_user: models.User = Depends(deps.get_current_user)):
    post = crud.get_post(db, post_id=post_id, user_id=current_user.id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or you do not have permission to respond to it.")
    
    crud.save_auto_response_settings(db=db, post_id=post_id, settings=auto_response)
    return {"message": "Automatic response settings updated successfully."}
