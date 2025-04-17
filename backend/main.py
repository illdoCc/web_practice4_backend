from fastapi import FastAPI, HTTPException, status, Request
from sqlalchemy import insert, select, update, delete
from myUser import User
from sqlalchemy import create_engine
from hashlib import sha256
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


engine = create_engine("postgresql://postgres:123@localhost:8080/test")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(username):
    to_encode = {
        'sub': '1234567890',
        'name': username,
        'iat': 1516239022
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





class UserLogin(BaseModel):
    username: str
    # password: str

@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    pwd = sha256(user.username.encode('utf-8')).hexdigest()
    # return {'AAA'}
    with engine.connect() as conn:
        
        # search user in db
        search_stmt = select(User).filter_by(username=user.username, password=pwd)
        result = conn.execute(search_stmt).fetchone()
        # return {'AAA'}
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # utcnow要加括號，因為是要update一個值，而非一個function
        update_stmt = update(User).where(User.username == user.username).values(last_login=datetime.utcnow())
        conn.execute(update_stmt)
        conn.commit()
        # create jwt token
        access_token = create_access_token(user.username)
        return {'access_token': access_token, 'token_type': 'bearer'}
    

@app.get("/user/", status_code=status.HTTP_200_OK)
async def getUser(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("name")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    with engine.connect() as conn:
        search_stmt = select(User).filter_by(username=username)
        user = conn.execute(search_stmt).fetchone()
    if not user:
        raise HTTPException(status_code=400, detail="Bad request")
    return dict(user._mapping)
    
@app.delete("/user/", status_code=status.HTTP_200_OK)
async def deleteUser(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("name")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    with engine.connect() as conn:
        search_stmt = select(User).filter_by(username=username)
        user = conn.execute(search_stmt).fetchone()
        if not user:
            raise HTTPException(status_code=400, detail="Bad request")
        delete_stmt = delete(User).where(User.username == username)
        conn.execute(delete_stmt)
        conn.commit()


class CreateOrChangeUser(BaseModel):
    username: str
    birthday: str

@app.post("/user/", status_code=status.HTTP_200_OK)
async def createUser(user: CreateOrChangeUser):
    pwd = sha256(user.username.encode('utf-8')).hexdigest()
    with engine.connect() as conn:
        search_stmt = select(User).filter_by(username=user.username)
        result = conn.execute(search_stmt).fetchone()
        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        insert_stmt = insert(User).values(username=user.username, password=pwd, birthday=user.birthday)
        conn.execute(insert_stmt)
        conn.commit()


@app.patch("/user/", status_code=status.HTTP_200_OK)
async def createUser(user: CreateOrChangeUser, request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("name")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # pwd = sha256(user.username.encode('utf-8')).hexdigest()
    with engine.connect() as conn:
        search_stmt = select(User).filter_by(username=user.username)
        # 檢查更改的名字是否已存在資料庫中
        if conn.execute(search_stmt).fetchone():
            raise HTTPException(status_code=400, detail="Bad request")
        pwd = sha256(user.username.encode('utf-8')).hexdigest()
        update_stmt = update(User).where(User.username == username).values(username=user.username, password=pwd, birthday=user.birthday)
        conn.execute(update_stmt)
        conn.commit()