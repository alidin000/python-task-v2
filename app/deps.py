# app/deps.py
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import crud, models, auth, database

def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        print(f"Decoded payload: {payload}")
        user_id: str = payload.get("sub")
        print(f"User ID extracted from token: {user_id}")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT decoding failed with error: {e}")
        raise credentials_exception


    user = crud.get_user(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

