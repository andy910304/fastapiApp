from typing import List

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from jose import JWTError, jwt
from datetime import datetime, timedelta
import shutil





models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/users/")
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(current_user = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/posts/")
def create_post(
    title: str, body: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id
    
    with open("media/" + file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
        
    url = str("media/" + file.filename)
    
    return crud.create_post(db = db, user_id = user_id, title = title, body = body, url=url)

@app.get("/posts/")
def post_list(db: Session = Depends(get_db)):
    return crud.post_list(db = db)

# @app.get("/posts/{post_id}")
# def post_detail(post_id:int, db: Session = Depends(get_db)):
#     return crud.get_post(db = db, id=post_id)

@app.get("/posts/{post_id}")
def post_detail(post_id:int, db: Session = Depends(get_db)):
    post = crud.get_post(db = db, id=post_id)
    comment = db.query(models.Comment).filter(models.Comment.post_id == post_id)
    active_comment =  comment.filter(models.Comment.is_active ==  True).all()
    
    if post is None:
        raise HTTPException(status_code=404, detail = "Este post no existe")
    
    return {"post" : post, "active_comment": active_comment}


@app.post("/posts/{post_id}/comment")
def create_comment(name:str, body: str, email: str, post_id: int, db: Session = Depends(get_db)):
        
    return crud.create_comment(db=db, post_id=post_id, name=name, body=body, email=email)